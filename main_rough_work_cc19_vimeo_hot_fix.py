import os 
import logging
import boto3
import botocore
import os
import json 
import time
import logging
import logging.handlers

from shutil import copyfile
import string 
import redis 
###AJM to be tidied up - fixing the problem of parse not being imported in python2  
#
#from urllib import parse

try:
    from urllib.parse import unquote 
except ImportError:
     from urlparse import unquote 


import sys
#sys.path.append('./youtube/')

from video_upload import youtube_video_upload, processing_youtube_url

sys.path.append('./logging/')
sts.path.append('./additional_processing/')
from vimeo_library import *

#from queuehandler import QueueHandler
#from logutils.queue import QueueHandler, QueueListener
from logging.handlers import QueueHandler, QueueListener
#####

import urllib
import requests
import os
import multiprocessing 
import logging
import pandas as pd
#import avenger_requests_1 as avenger_requests 
import avenger_requests_backoff_new_url as avenger_requests
from string import punctuation 

from moviepy.editor import *
#from moviepy.audio.io import AudioFileClip
import moviepy

import time
#from People_processing import *
from Email_processing import *
from People_processing_CC import *

#import Schedule as sch

#Variables for use in the code.

input_bucket = 'ds-ajm-videos'

exclusion_list = ['f2cdfee8-0ccc-46b3-945c-c7759ee755ea']


s3 = boto3.resource('s3')


#This sets the location of the local video files for processing 
#file_location = '~/Desktop/Testing_folder/{}'
file_location = '/home/ubuntu/AJM/video_files/'



def listener_configurer():
    root = logging.getLogger()
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
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            #######
            

def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    root.setLevel(logging.DEBUG)




def string_processing(s):
    s = ''.join(c for c in s if c not in punctuation)
    s = s.replace(' ','_') 
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
    my_bucket = s3.Bucket('ws18-videos')
    a = my_bucket.upload_file(file_location +'edited_videos/'+message, output_file_name)

    return a


def post_to_s3_audio(file_location, message, output_file_name):
    message = message.rstrip('.mp4') + '.mp3'
    my_bucket = s3.Bucket('ws18-videos')
    a = my_bucket.upload_file(file_location +'edited_videos/audio/'+message, 'audio/' + output_file_name)
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
        print('RESOLUTIONS DO NOT MATCH FOR {}'.format(process_name))
        ratio = starting_clip.size[0]/clip.size[0]
        clip = clip.resize(ratio)

    temp = video_file.split('_')
    start_time = temp[-2]
    end_time = temp[-1].rstrip('.mp4')
    if len(start_time) ==6  and len(end_time) ==6:
        start_time = (int(start_time[0:2]),int(start_time[2:4]),int(start_time[4:6]))
        end_time = (int(end_time[0:2]),int(end_time[2:4]),int(end_time[4:6]))
        clip = clip.subclip(start_time, t_end=None)
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


def audio_processing(video_file, output):
        try:
            temp = AudioFileClip(video_file)
        except:
            print('Oops, cannot process this audio file')
            logging.error('Failed to process audio for {}'.format(video_file))
        output = output.rstrip('.mp4') + '.mp3'
        temp.write_audiofile(output)



def processing_output_message(youtube_url, s3_url, uuid):
    message_attributes = {'youtube_url':{'DataType':'String','StringValue': youtube_url},
    's3_url':{'DataType':'String','StringValue': s3_url},
    'uid':{'DataType':'String', 'StringValue': uuid}}
    return message_attributes


def processing_audio_output_message(s3_url, uuid):
    message_attributes = { 's3_url':{'DataType':'String','StringValue': s3_url},
    'uid':{'DataType':'String', 'StringValue': uuid}}
    return message_attributes



def processing_message(queue, configurer, process_name, tasks, speaker_email_data, sting, watermark, slug, sheet_id, sheet_name):
    """
    Processes the message which is sent 
    """
    while True:
        configurer(queue)
        logger = logging.getLogger(__name__)


        r = redis.Redis(host='localhost', port = 6379, db=0)


        task = tasks.get()
        message = task[0]

        print(message)


        if message == 0:
            print('{} process quits'.format(process_name))
        else:
            print('{} recieved {}'.format(process_name,message))

    
            try:
                uuid = message.split('_')[-3]
                keys = r.keys()
                keys = [c.decode('utf-8') for c in keys]
                keys = [c for c in keys if uuid in c]

                if len(keys) != 1:
                    #raise Exception as e:
                    #    logger.exception(f'Failed to find unique key for{uuid}')
                    continue
                else:
                    key = keys[0]

            except Exception as e:
                logger.exception(f'Failed to find unique key for {uuid}')        

            try:
                r.hset(key,'status','UUID processed')

            except Exception as e:
                    logger.exception(f'Failed to updated Redis for {uuid}; Processing')


            try:
                block = r.hget(key,'block')
                if block == 1:
                    print(f'{process_name} with {uuid} has been blocked')  
                    continue
            
            except Exception as e:
                logger.exception(f'Failed to read block status for {uuid}')
                



#
#            try:
#                cell_range = 'I{0}:I{0}'.format(row)
##                flag = sch.read_single_range(sheet_id, cell_range)
#
#
#                if 'values' in flag.keys():
#                    flag = flag['values'][0][0]
#
#                    try:
#                        cell_range = 'K{0}:K{0}'.format(row)
##                        sch.write_single_range(sheet_id, cell_range,[['Upload Blocked']])
##                        print('{} BLOCKED'.format(process_name))
#
#                    except Exception as e:
#                        logging.error('Failed to update sheets for {}'.format(process_name))
#                        print('{} failed to update sheets'.format(process_name))
#
#                    continue
#
#            except Exception as e:
#                logging.error('Failed to read block status {}'.format(process_name))
#                print('{} failed to read block status'.format(process_name))
#
#

#####THIS IS JUST COMMENTED OUT ; DON'T KNOW WHAT IT WAS NEEDED FOR

#            try:
#                avenger = avenger_requests.avenger_requests(slug)
#                talk_location_id = avenger.get_timeslot_id(uuid)
#
#                try:
#                    r.hset(key,'status','Avenger lookup successful')
#                    print(f'Avenger lookup successful for {uuid}') 
#
#                except Exception as e:
#                    logging.error(f'Failed to update Redis for {uuid}; Avenger')
#                    print(f'{process_name} failed to update Redis; Avenger')
#
#            except Exception as e:
#                logger.error(f'Avenger lookup failed for {uuid}')
#                print(f'Avenger lookup failed for {uuid}')
#
#                try:
#                    r.hset(key,'status','Failed to process Avenger ID')
#
#                except Exception as e:
#                    logging.error(f'Failed to update sheets for {process_name}')
#                    print(f'Failed to update sheets for {process_name}')
#                continue

######THIS IS JUST COMMENTED OUT ; DON'T KNOW WHAT IT WAS NEEDED FOR

            try:
                retrieve_from_s3(message)
                
                try:
                    r.hset(key,'status','Recieved from S3')
                    print(f'Recieved {uuid} from S3 for {process_name}')

                except Exception as e:
                    logging.error(f'Failed to update Redis for {process_name}')
                    print(f'{process_name} failed to update Redis')


            except Exception as e:
               logger.error(f'Problem retrieving from S3 {uuid}')
               print(f'Problem retrieving from S3 {uuid}')

                
               try:
                   r.hset(key,'status','Failed to retrieve video from S3')
                   print(f'{process_name} failed to retrieve video from S3')

               except Exception as e:
                   logging.error(f'{process_name} failed to update sheets for {uuid}')
                   print(f'{process_name} failed to update Redis')

               continue 



            try:
                video_processing(process_name,file_location + message, sting,
                 watermark, file_location +'edited_videos/'+message)
                
                try:
                    print(f'Video processing successful')
                    r.hset(key,'status','Video processing complete') 

                except Exception as e:
                    logging.error(f'Failed to update Redis for {process_name}')
                    print(f'{process_name} failed to update Redis')



            except Exception as e:
                logger.error(f'{process_name} problem processing video {uuid}')
                print(f'{process_name} problem processing {uuid}')
                copyfile(file_location+message,file_location +'edited_videos/'+message)

                try:
                    r.hset(key,'status',f'{process_name} failed to update Redis')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update Redis')



            try:
                description = r.hget(key,'description')
                description = description.decode('utf-8')
                speakers = r.hget(key, 'speakers')
                speakers = speakers.decode('utf-8')
                speakers_for_emails = r.hget(key,'speakers_for_emails')
                speakers_for_emails = speakers_for_emails.decode('utf-8')
                speakers_for_youtube_tag = speakers_for_emails
                speakers_for_emails = speakers_for_emails.split(',')
                title = r.hget(key, 'title')
                title = title.decode('utf-8')
                title_for_youtube =  '#CollisionConf 2019 ' + title
                title = string_processing(title)
                description = speakers + ' \n' + description 



#            try:
#                description = avenger.description_processing(uuid)
#                description = description + '\n \nWish you were here? Sign up for 2 for 1 discount code for #WebSummit 2019 now: https://news.websummit.com/live-stream'
#                speakers = avenger.name_processing(uuid)
#                speakers_for_emails = avenger.speaker_names(uuid)
#                speakers_for_youtube_tag = str(', '.join(speakers_for_emails))
#                title = avenger.title_processing(uuid)
#                title_for_youtube = title
#                title = string_processing(title) 
#                description = speakers + ' \n ' + description

                
                
                try:
                    r.hset(key,'status','Metadata acquired')

                except Exception as e:
                    logging.error(f'{process_name} failed to update Redis')
                    print(f'{process_name} failed to update Redis')
            
            
            except Exception  as e:
                print('Failed to obtain metadata')
                logger.error(f'Failed to obtain metadata {message}')
            

                try:
                    r.hset(key,'status','Failed to obtain metadata')

                except Exception as e:
                    logging.error(f'Failed to update sheets for {process_name}')
                    print(f'{process_name} failed to update redis')


            try:
                audio_processing(file_location +'edited_videos/'+message, file_location +'edited_videos/audio/'+message)
                print('Audio processing successful')

                try:
                    r.hset(key,'status','Audio Processed')

                except Exception as e:
                    logging.error(f'Failed to update sheets for {process_name}')
                    print(f'{process_name} failed to update sheets')



                try:
                    post_to_s3_audio(file_location, message, uuid + '_' + title + '.mp3')

                    try:
                        r.hset(key,'status','Audio posted to S3') 

                    except Exception as e:
                        logging.error(f'Failed to update sheets for {process_name}')
                        print(f'{process_name} failed to update sheets')



                except Exception as e:    

                    
                    try:
                        r.hset(key,'status','Failed to post audio to S3') 

                    except Exception as e:
                        logging.error(f'Failed to update sheets for {process_name}')
                        print(f'{process_name} failed to update sheets')



            except Exception as e:
                logging.error(f'Problem with audio processing by {process_name}')


            try:
                #youtube_post = youtube_video_upload(file_location + 'edited_videos/' + message, title, description,'WebSummit','22','private')
                #youtube_post = youtube_video_upload(file= file_location + 'edited_videos/' + message,title= title_for_youtube, description=description,keywords='Web Summit, Collision, web summit conference, collision conference, web summit paddy, toronto, web summit youtube, collision toronto, {}'.format(speakers_for_youtube_tag),category='22',privacyStatus='public') 
                vimeo_post = vimeo_upload(file= file_location + 'edited_videos/' + message, title = title_for_youtube, description = description)

                try:
                    r.hset(key,'status','Posted to youtube')

                except Exception as e:
                    logging.error(f'Failed to update sheets for {process_name}')
                    print(f'{porcess_name} failed to update sheets')

                youtube_url = vimeo_post 

                try:
                    r.hset(key,'youtube_url', youtube_url)

                except Exception as e:
                    logging.error(f'Failed to update sheets for {process_name}')
                    print(f'{process_name} failed to update sheets')
 


            except:
                logger.error(f'Failed to post to youtube {message}')
                print('Failed to post to Youtube')


                try:
                    r.hset(key,'status','Failed to post to youtube')

                except Exception as e:
                    logging.error(f'Failed to update sheets for {process_name}')
                    print(f'{process_name} failed to update sheets')


                #continue
            
            #This is where we get the description and speakers for a talk and add
            # it to the facebook video            
            

            try: 
                post_to_s3(file_location,message, uuid + '_' + title + '.mp4')
                print('Successfully posted to S3') 
                
                
                try:
                    r.hset(key,'status','Posted to S3')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')
          
          
            except Exception as e:
                logger.error(f'Failed to post to S3 {message}')
                print('Failed to upload video to S3')


                try:
                    r.hset(key,'status','Failed to post to S3')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')




            try:
                os.remove(file_location + message)
                os.remove(file_location + 'edited_videos/' + message)
                os.remove(file_location +'edited_videos/audio/'+message.rstrip('.mp4') + '.mp3')
                print('removed local files')


                try:
                    r.hset(key, 'status', 'Removed local files')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')



            except:
                logger.error(f'Failed to delete the local copy of the file {message}')
                print('Failed to remove local copies')


                try:
                    r.hset(key, 'status', 'Failed to remove local files')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')


            #This is where we get the video url for the facebook video and email it
            #to the speakers

            try:   
                #youtube_url = processing_youtube_url(youtube_post)  #This was commented out - I do not know why 
                #youtube_url = uuid
                #print(youtube_url)
                youtube_url = 'Youtube not yet available'
                s3_url = 'https://s3-eu-west-1.amazonaws.com/ws18-videos/' + uuid + '_' + title + '.mp4' 
                s3_url_for_talks = s3_url 
                message_attributes = processing_output_message(youtube_url, s3_url, uuid)
                print(message_attributes)
                sqs = boto3.resource('sqs',region_name='eu-west-1')
                print('Resourse made')
                youtube_queue = sqs.get_queue_by_name(QueueName='Talkbot_output')
                print('Queue got')
                data = {}
                data['Body'] = message
                data = json.dumps(data)
                youtube_queue.send_message(MessageBody=data, MessageAttributes=message_attributes)
                print('Queue populated')


                try:
                    r.hset(key,'status','Avenger queue populated')                    
                    r.hset(key,'s3_url_video',s3_url)


                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')



            except Exception  as e:
                print('Failed to populate avenger queue')
                logging.error(f'Failed to populate avenger queue for {message}')


                try:
                    r.hset(key,'status','Avenger queue failed to populate')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')



            try:   
                s3_url = 'https://s3-eu-west-1.amazonaws.com/ws18-videos/audio/' + uuid + '_' + title + '.mp3'  
                sqs = boto3.resource('sqs',region_name='eu-west-1')
                print('Transcription resourse made')
                trans_queue = sqs.get_queue_by_name(QueueName='Talkbot_transcription')
                print('Transcription queue got')
                data = {}
                data['Body'] = {'uuid':uuid, 's3_url':s3_url, 'youtube_url':youtube_url}
                data = json.dumps(data)
                trans_queue.send_message(MessageBody=data)
                print('Transcription queue populated')


                try:
                    r.hset(key,'status','Transcription queue populated')
                    r.hset(key,'s3_url_transcription', s3_url)

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process} failed to update sheets')



            except Exception  as e:
                print(f'Failed to populate transcription queue for {message}')
                logger.error(f'Failed to populate transcription queue for {message}')


                try:
                    r.hset(key,'status','Avenger queue failed to populate')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')



#            time.sleep(10)

#            try:
#                for speaker in speakers_for_emails:
#                    emails = get_emails_cc(str(speaker), speaker_email_data)
#                    send_email_s3(emails[0],emails[1],s3_url_for_talks)
#                    #send_email(emails[0],emails[1],youtube_url) 
#                    time.sleep(5)
#
#
#                try:
#                    r.hset(key,'status','Speakers emailed')
#
#                except Exception as e:
#                    logging.error(f'{process_name} failed to update sheets')
#                    print(f'{process_name:} failed to update sheets')
#
#
#            except:
#                print('Emails have not been sent!')    
#                logging.error(f'failed to cc email {message}')
#
#
#                try:
#                    r.hset(key,'status','Speakers not emailed')
#
#                except Exception as e:
#                    logging.error(f'{process_name} failed to update sheets')
#                    print(f'{process_name} failed to update sheets')

            print(f'{process_name} process finishes {message}')

            
            try:
                r.hset(key,'status','Finished')

            except Exception as e:
                logging.error(f'{process_name} failed to update sheets')
                print(f'{process_name} failed to update sheets')



    return




def main(speaker_email_data, slug = 'ws18',watermark='./watermarks/MC_watermark.png',sting='./sting/MC_intro.mp4',sheet_name =
'WS_18_stages',sheet_id = '1LafAM4Ru3fZYEyt44J-Pixul0VV4Yfxmvu7hr5te-vg',free_cores=1):
    """
    Manages SQS and the multiprocessing section of the code


    Args:
        speaker_email_data (str): The csv file of the speaker email data.
        slug (str): The identifying slug for the conference used for the avenger module to obtain schedule, descriptions etc.
        watermark (str): The path of the watermark used to stamp the videos.
        sting (str): The path of the opening sting used to stamp the videos. Note the resolution of the sting sets the output resolution for the system.
        free_cores (int): The number of cores which will not be used by the multiprocessing module 

    Returns:
        None

    """





#Setting up the multiprocess processing part
    
    speaker_email_data = pd.read_csv(speaker_email_data)

    tasks = multiprocessing.Queue(-1) #was multiprocess

    logging_queue = multiprocessing.Queue(-1)
    
    
    listener = multiprocessing.Process(target=listener_process,
                                       args=(logging_queue, listener_configurer))

    listener.start()

    num_processes = multiprocessing.cpu_count() - free_cores 

    for i in range(num_processes):

        process_name = 'P{}'.format(str(i))

        new_process = multiprocessing.Process(target=processing_message, args=(logging_queue, worker_configurer,
        process_name, tasks, speaker_email_data, sting, watermark,slug, sheet_id, sheet_name))

        new_process.start()


#Setting up the connection to monitor SQS 

    sqs = boto3.resource('sqs',region_name = 'eu-west-1')
    q = sqs.get_queue_by_name(QueueName='DS_AJM_VIDEO')    



    while True:

        messages = []
        rs = q.receive_messages()
        for m in rs:
            temp = json.loads(m.body)
            m.delete()
            try:
                temp = temp['Records'][0]['s3']['object']['key']
                temp = unquote(temp)
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
    presets = eval(input('Would you like to continue with DEFAULTS(0) or user defined INPUTS(1)?:'))

    if presets == 0:
        speaker_email_data = './stages_speakers/CC19_emails.csv'
        slug = 'cc19'
        watermark = './watermarks/Collision_Logo_Colour.png'
        sting = './sting/CC19_video_intro_V01.mp4'

    elif presets == 1:
        speaker_email_data = input('Enter the full string path for the speaker email list:')
        sting = input('Enter the full string path for the sting:')
        watermark = input('Enter the full string path for the watermark:')

    else:
        print('Error - must enter eithe DEFAULTS or INPUTS')        
        exit()

    main(speaker_email_data, slug=slug, watermark=watermark, sting = sting)