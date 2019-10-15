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

try:
    from urllib.parse import unquote 
except ImportError:
     from urlparse import unquote 


import sys
#from urllib import parse
#sys.path.append('./youtube/')

from video_upload import youtube_video_upload, processing_youtube_url

sys.path.append('./logging/')
sys.path.append('./additional_processing/')
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
from string import punctuation 

from moviepy.editor import *
#from moviepy.audio.io import AudioFileClip
import moviepy

import time
#from People_processing import *
from Email_processing import *
from People_processing_CC import *

#Defining global variables
s3 = boto3.resource('s3')
r = redis.Redis(host='localhost', port = 6378, db=0,decode_responses=True) #Listening on non-standard port 6378
youtube_privacy_status = 'private'

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
            if record is None: 
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            

def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)

def string_processing(s):
    s = ''.join(c for c in s if c not in punctuation)
    s = s.replace(' ','_') 
    return s


def retrieve_from_s3(filename, input_bucket):
    """
    Retrieves a file from s3 bucket names ds-ajm-videos

    Returns
        bucket object
    """

    my_bucket = s3.Bucket(input_bucket)
    a = my_bucket.download_file(filename,file_location + filename.lstrip(input_bucket + '/'))
    return a    


def post_to_s3(file_location, message, output_file_name, output_bucket):
    my_bucket = s3.Bucket(output_bucket)
    a = my_bucket.upload_file(file_location +'edited_videos/'+message, output_file_name)

    return a


def post_to_s3_audio(file_location, message, output_file_name, audio_files_bucket):
    message = message.rstrip('.mp4') + '.mp3'
    my_bucket = s3.Bucket(audio_files_bucket)
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
        clip = clip.subclip(start_time, end_time)
        print('Clip successfully edited')
    else:
        print('Clip not edited ')

    logo = (ImageClip(watermark)
          .set_duration(clip.duration)
          .resize(height=50) 
          .margin(right=8, top=8,bottom =8, left = 8, opacity=0) 
          .set_pos(("right","top")))

    clip = CompositeVideoClip([clip, logo])

    clip = concatenate_videoclips([starting_clip,clip])    
    clip = moviepy.video.fx.all.fadein(clip,6)
    clip = moviepy.video.fx.all.fadeout(clip,6)
    clip.write_videofile(output, temp_audiofile="{}_temp-audio.m4a".format(process_name), 
    remove_temp=False, codec="libx264", audio_codec="aac")


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
    'vimeo_url':{'DataType':'String','StringValue': vimeo_url},
    's3_url':{'DataType':'String','StringValue': s3_url},
    'uid':{'DataType':'String', 'StringValue': uuid}}
    return message_attributes


def processing_audio_output_message(s3_url, uuid):
    message_attributes = { 's3_url':{'DataType':'String','StringValue': s3_url},
    'uid':{'DataType':'String', 'StringValue': uuid}}
    return message_attributes



def processing_message(queue, configurer, process_name, tasks, speaker_email_data, sting, watermark, sheet_id, sheet_name, input_bucket, output_bucket, audio_files_bucket):
    """
    Processes the message which is sent 
    """
    while True:
        configurer(queue)
        logger = logging.getLogger(__name__)




        task = tasks.get()
        message = task[0]

        print(message)


        if message == 0:
            print('{} process quits'.format(process_name))
        else:
            print('{} recieved {}'.format(process_name,message))

    
            try:
                message_retrieve = message.replace('- -','-+-')
                message = message_retrieve 
                message = message.lstrip(input_bucket + '/') 
                uuid = message.split('_')[-3]
                uuid = uuid.replace('- -','-+-')      

                keys = r.keys()
                keys = [c for c in keys if uuid in c]

                if len(keys) != 1:
                    raise Exception('No single key found')
                    logger.exception(f'Failed to find unique key for{uuid}')
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
                


            try:
                retrieve_from_s3(message_retrieve, input_bucket)
                
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
                speakers = r.hget(key, 'speakers')
                speakers_for_emails = r.hget(key,'speakers_for_emails')
                speakers_for_youtube_tag = speakers_for_emails
                speakers_for_emails = speakers_for_emails.split(',')
                title = r.hget(key, 'title')
                title_for_youtube =  title_lead_in + title
                title = string_processing(title)
                description = speakers + ' \n' + description 
                
                try:
                    r.hset(key,'status','Metadata acquired')
                    print(f"{process_name} aquired metadata")

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
                    post_to_s3_audio(file_location, message, uuid + '_' + title + '.mp3', audio_files_bucket)

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
                print(f'{pricess_name} failed to process audio')



            try:
                privacy = r.hget(key,'set_privacy')

 

                if privacy == 1:
                    vimeo_url = vimeo_upload(file_location + 'edited_videos/' + message, title_for_youtube, description, privacy = 'unlisted')
                    
                    try: 
                        r.hset(key,'status','Posted privately on Vimeo')

                    except Exception as e:
                        logging.error(f'Failed to update Redis for {process_name}')
                        print(f'{porcess_name} failed to update Redis')

                    try:
                        r.hset(key,'vimeo_link', vimeo_url)

                    except Exception as e:
                        logging.error(f'Failed to update sheets for {process_name}')
                        print(f'{process_name} failed to update sheets')                           


                if privacy == 1:
                    vimeo_url = vimeo_upload(file_location + 'edited_videos/' + message, title_for_youtube, description)
                    
                    try: 
                        r.hset(key,'status','Posted publicly on Vimeo')

                    except Exception as e:
                        logging.error(f'Failed to update Redis for {process_name}')
                        print(f'{porcess_name} failed to update Redis')

                    try:
                        r.hset(key,'vimeo_link', vimeo_url)

                    except Exception as e:
                        logging.error(f'Failed to update sheets for {process_name}')
                        print(f'{process_name} failed to update sheets')                           

                
                    
            except:
                logger.error(f'Failed to post to Vimeo {message}')
                print('Failed to post to Vimeo')


                try:
                    r.hset(key,'status','Failed to post to Vimeo')

                except Exception as e:
                    logging.error(f'Failed to update Redis for {process_name}')
                    print(f'{process_name} failed to update Redis')



            try:
               upload_to_youtube = r.hget(key,'upload_to_youtube')
               if upload_to_youtube == 1:
                   try:
                       youtube_upload = youtube_video_upload(file=file_location + 'edited_videos/' + message,title= title,
                        description= description,keywords='AJM F',category='22',privacyStatus=youtube_privacy_status)
                       youtube_url = processing_youtube_url(youtube_upload)

                       try:

                           r.hset(key,'youtube_link')

                       except Exception as e:
                           logging.error(f'{process_name} failed to update Redis with youtube link')
                           print(f'{process_name} failed to update Redis with youtube link')
                        

                   except Exception as e:
                        logging.error(f'{process_name} failed to upload to youtube')
                        print(f'{process_name} failed to upload to youtube')   

               else:
                    youtube_url = ''


            except Exception as e:
                logging.error(f'{process_name} failed to get youtube upload flag')
                youtube_url = ''
                pass

            try:
                post_to_s3(file_location,message, f'{uuid}_{title}.mp4',output_bucket)
                print('Successfully posted to S3') 
                
                
                try:
                    r.hset(key,'status','Posted to S3')

                except Exception as e:
                    logging.error(f'{process_name} failed to update Redis for S3 post')
                    print(f'{process_name} failed to update Redis for S3 post')
          
          
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
                youtube_url = vimeo_post
                s3_url = 'https://s3-eu-west-1.amazonaws.com/ws18-videos/' + uuid + '_' + title + '.mp4' 
                s3_url_for_talks = s3_url 
                message_attributes = processing_output_message(youtube_url, s3_url, uuid, vimeo_url)
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
                s3_url = f'https://s3-eu-west-1.amazonaws.com/{audio_files_bucket}/audio/{uuid}_{title}.mp3'  
                sqs = boto3.resource('sqs',region_name='eu-west-1')
                print('Transcription resourse made')
                trans_queue = sqs.get_queue_by_name(QueueName='Talkbot_transcription')
                print('Transcription queue got')
                data = {}
                data['Body'] = {'uuid':uuid, 's3_url':s3_url, 'youtube_url':youtube_url, 'vimeo_url':vimeo_url}
                data = json.dumps(data)
                trans_queue.send_message(MessageBody=data)
                print('Transcription queue populated')


                try:
                    r.hset(key,'status','Transcription queue populated')

                except Exception as e:
                    logging.error(f'{process_name} failed to update redis for transcription ')
                    print(f'{process} failed to update Redis for transcription')



            except Exception  as e:
                print(f'Failed to populate transcription queue for {message}')
                logger.error(f'Failed to populate transcription queue for {message}')


                try:
                    r.hset(key,'status','Avenger queue failed to populate')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')



            try:
                for speaker in speakers_for_emails:
                    emails = get_emails_cc(str(speaker), speaker_email_data)
                    #send_email_s3(emails[0],emails[1],s3_url_for_talks)
                    send_email(emails[0],emails[1],youtube_url) 
                    time.sleep(5)


                try:
                    r.hset(key,'status','Speakers emailed')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name:} failed to update sheets')


            except:
                print('Emails have not been sent!')    
                logging.error(f'failed to cc email {message}')


                try:
                    r.hset(key,'status','Speakers not emailed')

                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')

            print(f'{process_name} process finishes {message}')

            
            try:
                r.hset(key,'status','Finished')

            except Exception as e:
                logging.error(f'{process_name} failed to update sheets')
                print(f'{process_name} failed to update sheets')



    return




def main(speaker_email_data,input_bucket, output_bucket, audio_files_bucket, watermark='./watermarks/MC_watermark.png',sting='./sting/MC_intro.mp4',sheet_name =
'WS_18_stages',sheet_id = '1LafAM4Ru3fZYEyt44J-Pixul0VV4Yfxmvu7hr5te-vg',free_cores=1 ):
    """
    Manages SQS and the multiprocessing section of the code


    Args:
        speaker_email_data (str): The csv file of the speaker email data.
        watermark (str): The path of the watermark used to stamp the videos.
        sting (str): The path of the opening sting used to stamp the videos. 
            Note the resolution of the sting sets the output resolution for the system.
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
        process_name, tasks, speaker_email_data, sting, watermark, sheet_id, sheet_name,input_bucket, output_bucket, audio_files_bucket))

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
        speaker_email_data = './stages_speakers/RC19_emails.csv'
        watermark = './watermarks/RISE_Logo_Colour.png'
        sting = './sting/RISE_Preroll.mp4'
        input_bucket = 'ws19-raw-videos'
        output_bucket = 'ws19-proccessed-videos'
        audio_files_bucket = 'ws19-audio'
        file_location = '/home/ubuntu/AJM/video_files/'
        title_lead_in = ''

    elif presets == 1:
        speaker_email_data = input('Enter the full string path for the speaker email list:')
        sting = input('Enter the full string path for the sting:')
        watermark = input('Enter the full string path for the watermark:')

    else:
        print('Error - must enter eithe DEFAULTS or INPUTS')        
        exit()

    main(speaker_email_data, watermark=watermark, sting = sting, input_bucket = input_bucket, output_bucket = output_bucket, audio_files_bucket = audio_files_bucket)