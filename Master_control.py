"""
A script to monitor the upload of videos to the S3 bucket
"""

import boto.sqs
import os 
import logging
import boto3
import botocore
import os
import json 
import time
from urllib import parse
import requests
import os 
from subprocess import call
from moviepy.editor import *
import moviepy

import time
from People_processing import *
from Email_processing import * 
bucket_name = 'ds.ajm.videos'
#path_to_videos = "/Users/aaronmeagher/AJM/video_files/"'
path_to_videos = "/home/ubuntu/AJM/video_files/"
s3 = boto3.resource('s3')

access_token_2 = os.environ['ACCESSTOKEN_VIDEO_2']
#file_location = '~/Desktop/Testing_folder/{}'
file_location = '/home/ubuntu/AJM/video_files/'


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/myapp.log',
                    filemode='w')



def retrieve_from_s3(filename):
    my_bucket = s3.Bucket('ds.ajm.videos')
    a = my_bucket.download_file(filename,path_to_videos + filename)
    call(['cp',path_to_videos + filename,path_to_videos + filename + 'copy'])
    return a    


def initialise_connection():
    try:
        conn = boto.sqs.connect_to_region(
        "eu-west-1",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET_KEY'])

    except KeyError as ke:
        logging.error('A keyerror {} has occured'.format(ke))

    return conn


def upload_video(video_path):
    """
    Json body contains the id of the facebook video which has been uploaded.
    """
    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token_2) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file) 
    return flag


def adding_description(post_id,description):
    """
    The return is either true or false.
    """
    data = {'description':description}
    url = 'https://graph.facebook.com/v2.10/{}?access_token={}'.format(post_id,access_token_2)
    flag = requests.post(url,json=data)
    return flag


def reading_video_url(post_id):
    url = 'https://graph.facebook.com/v2.10/{}?fields=permalink_url&access_token={}'.format(post_id,access_token_2)
    flag = requests.post(url)
    flag = 'www.facebook.com'+flag.json()['permalink_url']
    return flag

def video_processing(video_file, output, start_time = 0, end_time = 10):

    clip = VideoFileClip(video_file)
#    clip = clip.subclip(start_time,end_time)
    clip = moviepy.video.fx.all.fadein(clip,3)
    clip = moviepy.video.fx.all.fadeout(clip,3)
    clip.write_videofile(output, progress_bar = True, verbose = True)

def message_processing(message):
            retrieve_from_s3(message)
            video_processing(file_location+message,file_location+'edited_videos/'+message)
            post = upload_video(file_location+'edited_videos/'+message)
            description = get_description(message, speaker_talk_sheet)
            adding_description(post.json()['id'], description)
            video_url = reading_video_url(post.json()['id'])
            people_to_be_emailed = get_speakers(message, speaker_talk_sheet)
            emails = get_emails(people_to_be_emailed, speaker_email_sheet) 
            for email in emails:
                send_email(email,video_url)



if __name__ == '__main__':

#Setting up the connection to monitor SQS 

    conn = initialise_connection()
    q = conn.create_queue('DS_AJM_VIDEO')
    i = 0

    while True:
        if i % 60 == 0:
            print('Acquiring sheets')
            speaker_talk_sheet, speaker_email_sheet = get_spreadsheets()
            i = 0
            print('Sheets acquired')
        i = i+1

        messages = []
        rs = q.get_messages()
        for m in rs:
            temp = json.loads(m.get_body())
            print(m.get_body())
            print(temp)
            q.delete_message(m)
            try:
                temp = temp['Records'][0]['s3']['object']['key']
                temp = parse.unquote(temp)
                temp = temp.replace('+',' ')
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            messages.append(temp)

        for message in messages:
            message_processing(message)


        i = i + 1        
        time.sleep(60)




