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



access_token = os.environ['ACCESSTOKEN_VIDEO_2']
#file_location = '~/Desktop/Testing_folder/{}'
file_location = '/mnt/'


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/myapp.log',
                    filemode='w')





def retrieve_from_s3(filename):
    os.system('s4cmd get s3://ds.ajm.videos/{} \
    ~/Desktop/Testing_folder/{}'.format(filename,filename))


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
    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token_2) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file) 
    return flag


def adding_description(post_id,description):
    data = {'description':description}
    url = 'https://graph.facebook.com/v2.10/{}?access_token={}'.format(post_id,access_token)
    flag = requests.post(url,json=data)
    return flag

def video_processing(video_file,start_time, end_time,output):

    clip = VideoFileClip(video_file)
    clip = clip.subclip(start_time,end_time)
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
            q.delete_message(m)
            try:
                temp = temp['Records'][0]['s3']['object']['key']
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            messages.append(temp)

        for message in messages:
            retrieve_from_s3(message)
            upload_video(file_location+message)        


        time.sleep(60)




