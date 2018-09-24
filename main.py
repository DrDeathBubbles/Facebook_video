import boto.sqs
import os 
import logging
import boto3
import botocore
import os
import json 
import time



###AJM to be tidied up - fixing the problem of parse not being imported in python2  
#
#from urllib import parse

try:
    from urllib.parse import unquote 
except ImportError:
     from urlparse import unquote 


import sys
sys.path.append('./youtube/')

from video_upload import youtube_video_upload

#####

import urllib
import requests
import os
import multiprocessing 
import logging
import pandas as pd
import avenger_requests 
from string import punctuation 

from moviepy.editor import *
import moviepy

import time
from People_processing import *
from Email_processing import *
from People_processing_CC import *


#Variables for use in the code.

input_bucket = 'ds-ajm-videos'

exclusion_list = ['f2cdfee8-0ccc-46b3-945c-c7759ee755ea']


s3 = boto3.resource('s3')


#This sets the location of the local video files for processing 
#file_location = '~/Desktop/Testing_folder/{}'
file_location = '/home/ubuntu/AJM/video_files/'


#logging.basicConfig(level=logging.INFO,
#                    format='%(asctime)s %(levelname)s %(message)s',
#                    #filename='/home/ubuntu/AJM/video_files/talkbot.log',
#                    filename = './talkbot.log',
#                    filemode='w')


def listener_configurer():
    root = logging.getLogger()
    #h = logging.handlers.RotatingFileHandler('mptest.log', 'a', 300, 10)
    h = logging.handlers.RotatingFileHandler('mptest.log', 'a')
    f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    root.addHandler(h)


def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            ######AJM THIS NEEDS TO BE PUT BACK IN - WORKS IN PYTHON3 NOT PYTHON2
            #print('Whoops! Problem:', file=sys.stderr)
            #traceback.print_exc(file=sys.stderr)
            #######

def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    root.setLevel(logging.DEBUG)




def string_processing(s):
    s = ''.join(c for c in s if c not in punctuation)
    s = s.replace(' ','_') + '.mp4'
    return s



def retrieve_from_s3(filename):
    """
    Retrieves a file from s3 bucket names ds-ajm-videos

    Returns

    """

    my_bucket = s3.Bucket('ds-ajm-videos')
    a = my_bucket.download_file(filename,file_location + filename)
    return a    


def post_to_s3(file_location, message, output_file_name):
    my_bucket = s3.Bucket('rise18-videos')
    a = my_bucket.upload_file(file_location +'edited_videos/'+message, output_file_name)

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


def video_processing(process_name,video_file,sting, watermark, output):
    clip = VideoFileClip(video_file)
    starting_clip = VideoFileClip(sting)
    if clip.size[0] != starting_clip.size[0]:
        print('Resolutions do not match! Rescaling input video')
        ratio = starting_clip.size[0]/clip.size[0]
        clip = clip.resize(ratio)

    temp = video_file.split('_')
    start_time = temp[-2]
    end_time = temp[-1].rstrip('.mp4')
    if len(start_time) ==6  and len(end_time) ==6:
        start_time = (int(start_time[0:2]),int(start_time[2:4]),int(start_time[4:6]))
        end_time = (int(end_time[0:2]),int(end_time[2:4]),int(end_time[4:6]))
        clip = clip.subclip(start_time,end_time)
        print('clip_edited if loup')
    else:
        print('clip not edited ')

    logo = (ImageClip(watermark)
          .set_duration(clip.duration)
          .resize(height=50) 
          .margin(right=8, top=8,bottom =8, left = 8, opacity=0) 
          .set_pos(("right","top")))

    clip = CompositeVideoClip([clip, logo])

    clip = concatenate_videoclips([starting_clip,clip])    
    clip = moviepy.video.fx.all.fadein(clip,6)
    clip = moviepy.video.fx.all.fadeout(clip,6)
    clip.write_videofile(output, temp_audiofile="{}_temp-audio.m4a".format(process_name), remove_temp=False, codec="libx264", audio_codec="aac")


def processing_output_message(facebook_url, s3_url, uuid):
    message_attributes = {'facebook_url':{'DataType':'String','StringValue': facebook_url},
    's3_url':{'DataType':'String','StringValue': s3_url},
    'uid':{'DataType':'String', 'StringValue': uuid}}
    return message_attributes

def processing_message(queue, configure, process_name, tasks, results, speaker_email_data, sting, watermark, slug):
    """
    Processes the message which is sent 
    """
    while True:
        task = tasks.get()
        message = task[0]
        configure(queue)
        logger = logging.getLogger('main_logger')
        level = logging.INFO

        if message == 0:
            print('{} process quits'.format(process_name))
        else:
            print('{} recieved {}'.format(process_name,message))
            try:
                retrieve_from_s3(message)
                print('{} retrieves from S3'.format(process_name))
            except Exception as e:
               logger.log(logging.ERROR,'Problem retrieving {}'.format(message))
               print('Problem retrieving {}'.format(message))
               continue 


            try:
                uuid = message.split('_')[-3]
                if uuid in exclusion_list:
                    print('Exclusion found!')
                    continue
                avenger = avenger_requests.avenger_requests()
                talk_location_id = avenger.get_timeslot_id(uuid)
            except Exception as e:
                logger.log(logging.ERROR,'Failed to get the credentials for {}'.format(message))
                print('Failed to get credentials')
                continue 


            try:
                video_processing(process_name,file_location+message, sting, watermark, file_location +'edited_videos/'+message)
                print('Video processing successful')
            except Exception as e:
                logger.log(logging.ERROR,'Problem processing {}'.format(message))
                print('Problem processing {}'.format(message))
                os.rename(file_location+message,file_location +'edited_videos/'+message)

            print('{} processed video'.format(process_name))           


            #This is where we process the message and get information regarding the fb_page_id
            # and the access_token needed for the rest of the upload 


            
            try:
                post = upload_video(file_location + 'edited_videos/' + message, fb_page_id, access_token)
                if post.status_code == '400':
                    print('Uploads are blocked')
                    time.sleep(60*60*6)
                    continue
           
            except:
                logger.log(logging.ERROR,'Failed to post to facebook {}'.format(message))
                print('Failed to post to facebook')
                continue
            
            #This is where we get the description and speakers for a talk and add
            # it to the facebook video            
            
            try:
                description = avenger.description_processing(uuid)
                speakers = avenger.name_processing(uuid)
                title = avenger.title_processing(uuid)
                title = string_processing(title) 
                description = speakers + ' \n ' + description
                print(description)
                adding_description(post.json()['id'], description, access_token)

            except Exception  as e:
                print('Failed to add description')
                logger.log(logging.ERROR, 'Failed to add description {}'.format(message))
                logging.error(e)

            try: 
                post_to_s3(file_location,message, uuid + '_' + title)
                print('Successfully posted to S3') 
            except Exception as e:
                logger.log(logging.ERROR,'Failed to post to S3 {}'.format(message))
                print('Failed to upload video to S3')


            try:
                os.remove(file_location + message)
                os.remove(file_location + 'edited_videos/' + message)
                print('removed local files')

            except:
                logger.log(logging.ERROR,'Failed to delete the local copy of the file {}'.format(message))
                print('Failed to remove local copies')

            #This is where we get the video url for the facebook video and email it
            #to the speakers

            try:    
                facebook_url = reading_video_url(post.json()['id'], access_token)
                print(facebook_url)
                s3_url = 'https://s3-eu-west-1.amazonaws.com/cc18-videos/' + uuid + '_' + title   
                message_attributes = processing_output_message(facebook_url, s3_url, uuid)
                print(message_attributes)
                sqs = boto3.resource('sqs',region_name='eu-west-1')
                print('Resourse made')
                queue = sqs.get_queue_by_name(QueueName='Talkbot_output')
                print('Queue got')
                data = {}
                data['Body'] = message
                data = json.dumps(data)
                queue.send_message(MessageBody=data, MessageAttributes=message_attributes)
                print('Queue populated')

            except Exception  as e:
                print('Failed to email speakers')
                logger.log(logging.ERROR, 'Failed to email speakers for {}'.format(message))
                logging.error(e)

            time.sleep(5*60)
            try:
                t1 = speakers.split(',')
                t2 = t1[-1].split('and')
                t1.pop(-1)
                [t1.append(j) for j in t2] 
                t1 = [i.strip() for i in t1]
                for speaker in t1:
                    emails = get_emails_cc(speaker, speaker_email_data)
                    send_email_cc_2(emails[0],emails[1],facebook_url) 
                    time.sleep(5)

            except:
                print('emails have not been sent!')    
                logger.log(logging.ERROR, 'failed to cc email {}'.format(message))



            print('{} process finishes {}'.format(process_name, message))
    return




def main(speaker_email_data, slug = 'monc17',watermark='./watermarks/MC_watermark.png',sting='./sting/MC_intro.mp4',free_cores=1):
    """
    Manages SQS and the multiprocessing section of the code


    Args:
        speaker_email_data (str): The csv file of the speaker email data
        free_cores (int): The number of cores which will not be used by the multiprocessing module 

    Returns:
        None

    """

#Setting up the multiprocess processing part
    manager = multiprocessing.Manager()
    
    speaker_email_data = pd.read_csv(speaker_email_data)

    tasks = manager.Queue()
    results = manager.Queue()

    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(target=listener_process,
                                       args=(queue, listener_configurer))

    listener.start()

    num_processes = multiprocessing.cpu_count() - free_cores 

    for i in range(num_processes):

        process_name = 'P{}'.format(str(i))

        new_process = multiprocessing.Process(target=processing_message, args=(queue, worker_configurer, process_name, tasks, results, speaker_email_data, sting, watermark,slug))

        new_process.start()


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
                ###AJM commenting out and changing due to difficulty importing 
                #temp = parse.unquote(temp)
                temp = unquote(temp)
                ###
                temp = temp.replace('+',' ')
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            messages.append(temp)

        for message in messages:
            print(message)
            tasks.put([message])

        time.sleep(5)



if __name__ == '__main__':
    presets = input('Would you like to continue with DEFAULTS(0) or user defined INPUTS(1)?:')

    if presets == 0:
        speaker_email_data = './stages_speakers/Speakers_testing.csv'

    elif presets == 1:
        speaker_email_data = input('Enter the full string path for the speaker email list:')
        sting = input('Enter the full string path for the sting:')
        watermark = input('Enter the full string path for the watermark:')

    else:
        print('Error - must enter eithe DEFAULTS or INPUTS')        
        exit()

    main(speaker_email_data)