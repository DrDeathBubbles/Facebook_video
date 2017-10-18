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

import requests
import os 

from moviepy.editor import *
import moviepy

import time

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


#def retrieve_from_s3(filename):
#    os.system('s4cmd get s3://ds.ajm.videos/{} \
#    ~/video_files/{}'.format(filename,filename))
#


def retrieve_from_s3(filename):
    my_bucket = s3.Bucket('ds.ajm.videos')
    a = my_bucket.download_file(filename,path_to_videos + filename)
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

def video_processing(video_file, output, start_time = 0, end_time = 10):

    clip = VideoFileClip(video_file)
#    clip = clip.subclip(start_time,end_time)
    clip = moviepy.video.fx.all.fadein(clip,3)
    clip = moviepy.video.fx.all.fadeout(clip,3)
    clip.write_videofile(output)

if __name__ == '__main__':

#Setting up the connection to monitor SQS 

    conn = initialise_connection()
    q = conn.create_queue('DS_AJM_VIDEO')

    while True:
        messages = []
        rs = q.get_messages()
        for m in rs:
            temp = json.loads(m.get_body())
            print(temp)
            q.delete_message(m)
            try:
                temp = temp['Records'][0]['s3']['object']['key']
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            messages.append(temp)

        for message in messages:
            retrieve_from_s3(message)
            video_processing(file_location+message,file_location+message)
            post = upload_video(file_location+message)
            adding_description(post.json()['id'],'This is a test of the automated tagging of videos')



        time.sleep(60)




