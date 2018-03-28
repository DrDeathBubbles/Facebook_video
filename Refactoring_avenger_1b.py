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
import urllib
import requests
import os
import multiprocessing 
import logging
import pandas as pd
import avenger_requests 


from moviepy.editor import *
import moviepy

import time
from People_processing import *
from Email_processing import *


bucket_name = 'ds-ajm-videos'
#path_to_videos = "/Users/aaronmeagher/AJM/video_files/"'
path_to_videos = "/home/ubuntu/AJM/video_files/"
s3 = boto3.resource('s3')


#This is the access token for the test facebook video site
access_token_2 = os.environ['ACCESSTOKEN_VIDEO_2']

#This is the access token for the WebSummit HQ video site
access_token = os.environ['ACCESSTOKEN_WEB_SUMMIT_HQ']

#file_location = '~/Desktop/Testing_folder/{}'
file_location = '/home/ubuntu/AJM/video_files/'


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    #filename='/home/ubuntu/AJM/video_files/talkbot.log',
                    filename = './talkbot.log',
                    filemode='w')



def retrieve_from_s3(filename):
    """
    Retrieves a file from s3 bucket names ds-ajm-videos

    Returns

    """

    my_bucket = s3.Bucket('ds-ajm-videos')
    a = my_bucket.download_file(filename,path_to_videos + filename)
    return a    


def post_to_s3(file_location,message):
    my_bucket = s3.Bucket('ws17-videos')
    a = my_bucket.upload_file(file_location +'edited_videos/'+message,message)
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


#def upload_video(video_path):
#    """
#    Json body contains the id of the facebook video which has been uploaded.
#    """
#    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token_2) 
#    _file = {'file':open(video_path,'rb')}
#    flag = requests.post(url,files=_file) 
#    return flag

#def upload_video(video_path):
#    """
#    Returns {'id': '1450967228357958'}
#    """
#    url = 'https://graph-video.facebook.com/WebSummitHQ/videos?access_token={}'.format(access_token) 
#    _file = {'file':open(video_path,'rb')}
#    flag = requests.post(url,files=_file) 
#    return flag



def upload_video(video_path, fb_page_id, access_token):
    """
    Returns {'id': '1450967228357958'}
    """
    url = 'https://graph-video.facebook.com/{}/videos?access_token={}'.format(fb_page_id, access_token) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file)
    try:
        flag.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Http error {}'.format(err)) 
    return flag





def adding_description(post_id,description, access_token):
    """
    The return is either true or false.
    """
    data = {'description':description}
    url = 'https://graph.facebook.com/v2.10/{}?access_token={}'.format(post_id, access_token)
    flag = requests.post(url,json=data)
    return flag


def reading_video_url(post_id):
    url = 'https://graph.facebook.com/v2.10/{}?fields=permalink_url&access_token={}'.format(post_id, access_token)
    flag = requests.post(url)
    flag = 'www.facebook.com'+flag.json()['permalink_url']
    return flag


def video_processing(video_file, output):
    clip = VideoFileClip(video_file)

    temp = video_file.split('_')
    start_time = temp[4]
    end_time = temp[5].rstrip('.mp4')

    if len(start_time) ==6  and len(end_time) ==6:
        start_time = (int(start_time[0:2]),int(start_time[2:4]),int(start_time[4:6]))
        end_time = (int(end_time[0:2]),int(end_time[2:4]),int(end_time[4:6]))
        clip = clip.subclip(start_time,end_time)

    clip = moviepy.video.fx.all.fadein(clip,3)
    clip = moviepy.video.fx.all.fadeout(clip,3)
    clip.write_videofile(output, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

def speaker_formatting(speaker_list):
    if len(speaker_list) == 1:
        temp = speaker_list[0]
        return temp 

    if len(speaker_list) == 2:
        temp = speaker_list[0] + ' & ' + speaker_list[1]
        return temp 

    if len(speaker_list) > 2:
        temp = ', '.join(speaker_list[:-1]) + ' & ' + speaker_list[-1]
        return temp

def processing_message(process_name,tasks,results):
    """
    Processes the message which is sent 
    """
    while True:
        task = tasks.get()
        message = task[0]
        #speaker_talk_sheet = task[1]
        #speaker_email_sheet = task[2]
        
        if message == 0:
            print('{} process quits'.format(process_name))
        else:
            print('{} recieved {}'.format(process_name,message))
            try:
                retrieve_from_s3(message)
                print('{} retrieves from S3'.format(process_name))
            except Exception as e:
               logging.error('Problem retrieving {}'.format(message))
               logging.error(e)
               print('Problem retrieving {}'.format(message))
               continue 
            
            try:
                video_processing(file_location+message,file_location +'edited_videos/'+message)
                print('Video processing successful')
            except Exception as e:
                logging.error('Problem processing {}'.format(message))
                print('Problem processing {}'.format(message))
                logging.error(e)
                os.rename(file_location+message,file_location +'edited_videos/'+message)

            print('{} processed video'.format(process_name))           

            try: 
                post_to_s3(file_location,message)
                print('Successfully posted to S3') 
            except Exception as e:
                logging.error('Failed to post to S3')
                print('Failed to upload video to S3')
                logging.error(e)


            #This is where we process the message and get information regarding the fb_page_id
            # and the access_token needed for the rest of the upload 

            try:
                data = pd.read_csv('CC_18_access_tokens.csv')
                uuid = message.split('_')[3]
                avenger = avenger_requests.avenger_requests()
                talk_location_id = avenger.get_timeslot_id(uuid)
                fb_page_id = int(data[data['id']==talk_location_id]['page_id'])
                access_token = data[data['id']==talk_location_id]['long_lasting_token'].values[0]

            except Exception as e:
                logging.error('Failed to get the credentials')
                print('Failed to get credentials')
                continue 


            try:
                post = upload_video(file_location + 'edited_videos/' + message, fb_page_id, access_token)
                #if post.status_code == '400':
                #    print('Uploads are blocked')
                #    time.sleep(60*60*6)
                #    continue
           
            #except:
            #    logging.error('Failed to post to facebook')
            #    print('Failed to post to facebook')
            #    logging.error(e)
            #    continue

            except:
                print('Failed to post to Facebook 2')



            try:
                os.remove(file_location + message)
                os.remove(file_location + 'edited_videos/' + message)
                print('removed local files')

            except:
                logging.error('Failed to delete the local copy of the file')
                print('Failed to remove local copies')
            
            
            #This is where we get the description and speakers for a talk and add
            # it to the facebook video            
            
            try:
                description = avenger.get_description(uuid)
                speakers = avenger.name_processing(uuid)
                #description, location = get_description(message, speaker_talk_sheet)
                #people_to_be_emailed = get_speakers(message, speaker_talk_sheet)
                #speakers_formatted = speaker_formatting(people_to_be_emailed) 
                description = speakers + ' \n ' + description
                adding_description(post.json()['id'], description, access_token)

            except Exception  as e:
                print('Failed to add description')
                logging.error('Failed to add description')
                logging.error(e)


            #This is where we get the video url for the facebook video and email it
            #to the speakers

            try:    
                video_url = reading_video_url(post.json()['id'])
                print(video_url)
                #emails = get_emails(people_to_be_emailed, speaker_email_sheet) 
                #print(emails)
                #results.put(emails)
                #for email in emails:
                #    send_email(email,video_url)

            except Exception  as e:
                print('Failed to email speakers')
                logging.error('Failed to email speakers for {}'.format(message))
                logging.error(e)
            
            #try:
            #    update_spreadsheet(location, video_url)
            #    print('updated spreadsheets successfully')

            #except Exception as e:
            #    logging.error('Failed to update spreadsheet') 
            #    print('Failed to update spreadsheets')

            
            print('{} process finishes {}'.format(process_name, message))
    return


if __name__ == '__main__':

#Setting up the multiprocess processing part
    manager = multiprocessing.Manager()
    
    tasks = manager.Queue()
    results = manager.Queue()

    num_processes = 8

    pool = multiprocessing.Pool() 

    for i in range(num_processes):



        process_name = 'P{}'.format(str(i))

        new_process = multiprocessing.Process(target=processing_message, args=(process_name, tasks, results))

        new_process.start()


#Setting up the connection to monitor SQS 

    conn = initialise_connection()
    q = conn.create_queue('DS_AJM_VIDEO')
   # i = 0

    while True:
#        if i % 60*12 == 0:
#            print('Acquiring sheets')
#            speaker_talk_sheet, speaker_email_sheet = get_spreadsheets()
#            i = 0
#            print('Sheets acquired')
#        i = i+1

        messages = []
        rs = q.get_messages()
        for m in rs:
            temp = json.loads(m.get_body())
            q.delete_message(m)
            try:
                temp = temp['Records'][0]['s3']['object']['key']
                temp = parse.unquote(temp)
                temp = temp.replace('+',' ')
                #temp = temp.replace(':',' ')
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            messages.append(temp)

        for message in messages:
            print(message)
            tasks.put([message])

        i = i + 1        
        time.sleep(5)


