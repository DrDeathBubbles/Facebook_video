import sys
sys.path.append('./logging/')
sys.path.append('./additional_processing/')
sys.path.append('/home/ubuntu/Transcription/talkbot_transcription/source/')

import os 
import logging
import boto3
import json 
import time
import logging
import logging.handlers
import moviepy
import redis 
import urllib
import requests
import multiprocessing 
import pandas as pd
import glob


from logging.handlers import QueueHandler, QueueListener
from shutil import copyfile
from string import punctuation
from Transcription_control import generate_transcription_translate 
from vimeo_library import *
from moviepy.editor import *


try:
    from urllib.parse import unquote 
except ImportError:
     from urlparse import unquote 


s3 = boto3.resource('s3')
r = redis.Redis(host='localhost', port = 6378, db=0,decode_responses=True) #NOTE :Listening on non-standard port 6378]
languages = ['pt','es','de','fr']
sheet_data = pd.read_excel('./CFH_data.xlsx', sheet_name = None)

def sheets_processing_uid(sheet_data, message):
    index = message.split('_')[0]
    sheet_data['INDEX_RO']['Indec_number'] = sheet_data['INDEX_RO']['Index'].str.split(' ', expand = True)[0]
    out = sheet_data['INDEX_RO'][sheet_data['INDEX_RO']['Indec_number'] == index]
    return out['Title (55 Characters)'].values[0]



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
    a = my_bucket.upload_file(file_location + message, output_file_name)
    return a


def upload_to_s3(upload_file, bucket, upload_file_name):
    out = s3.meta.client.upload_file(upload_file,bucket,upload_file_name)
    return out


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



def processing_output_message(youtube_url, s3_url, uuid, vimeo_url):
    message_attributes = {'youtube_url':{'DataType':'String','StringValue': youtube_url},
    'vimeo_url':{'DataType':'String','StringValue': vimeo_url},
    's3_url':{'DataType':'String','StringValue': s3_url},
    'uid':{'DataType':'String', 'StringValue': uuid}}
    return message_attributes


def processing_output_babble(s3_url, uuid, vimeo_url, speakers, text, title):
    message_attributes = {
    'vimeo_url':{'DataType':'String','StringValue': vimeo_url},
    's3_url':{'DataType':'String','StringValue': s3_url},
    'uid':{'DataType':'String', 'StringValue': uuid},
    'speakers':{'DataType':'String','StringValue': speakers},
    'text':{'DataType':'String','StringValue': text},
    'title':{'DataType':'String','StringValue': title}}
    return message_attributes    

def clean_up(file_locations, key):
    for file_location in file_locations:
        files = glob.glob(file_location + f'*{key}*')
        for f in files:
            os.remove(f)



def processing_message(queue, configurer, process_name, tasks, input_bucket, output_bucket):
    """
    Processes the message which is sent 
    """
    while True:
        configurer(queue)
        logger = logging.getLogger(__name__)
        vimeo_url = 'Not Available'
        youtube_url = 'Not Available'


        task = tasks.get()
        message = task[0]



        if message == 0:
            print('{} process quits'.format(process_name))
        else:
            print('{} recieved {}'.format(process_name,message))


            key, uuid, message = task

            print(f'key {key}, uuid {uuid}, message {message}')


            try:
                retrieve_from_s3(message, input_bucket)
                
                try:
                    r.hset(key,'status','Recieved from S3')
                    r.hset(key,'s3_link_raw',f'https://s3-eu-west-1.amazonaws.com/{input_bucket}/{message}')
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
                   logging.error(f'{process_name} failed to update Redis for {uuid}')
                   print(f'{process_name} failed to update Redis')

               continue 




            try:
                description = r.hget(key,'description')
                speakers = r.hget(key, 'speakers')
                speakers_for_emails = r.hget(key,'speakers_for_emails')
                speakers_for_youtube_tag = speakers_for_emails
                speakers_for_emails = speakers_for_emails.split(',')
                title = r.hget(key, 'title')
                title_for_videos = title
                title = string_processing(title)
                description = speakers + ' \n' + description 
                print(title)


                description = ""
                speakers = ""
                speakers_for_emails = ""
                speakers_for_youtube_tag = ""
                title = sheets_processing_uid(sheet_data, message)

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
                region = 'eu-west-1'
                infile = message
                sub_files = generate_transcription_translate(region, input_bucket + '/', infile, languages, translate = False)
            except:

                print('Problem making subtitle files')

            try:
                upload_to_s3(sub_files[2], output_bucket,'transcription/' + sub_files[2])

                for sub in sub_files[0].values():
                    upload_to_s3(sub, output_bucket ,'vtt/' + sub)

                for sub in sub_files[1].values():
                    upload_to_s3(sub, output_bucket ,'srt/' + sub)    

            except:
                print('Sub files not uploaded')
                pass    

            try:
                privacy = int(r.hget(key,'set_private'))
                privacy = 1 ### AJM CFH forcing private during upload
                print(privacy)



                if privacy == 1:
                    print('uploading to vimeo')
                    vimeo_url = vimeo_upload(file_location + message, title_for_videos, description, privacy = 'unlisted')
                    print('Uploaded to vimeo')
                    
                    try: 
                        r.hset(key,'status','Posted privately on Vimeo')

                    except Exception as e:
                        logging.error(f'Failed to update Redis for {process_name}')
                        print(f'{process_name} failed to update Redis')

                    try:
                        r.hset(key,'vimeo_link', vimeo_url)

                    except Exception as e:
                        logging.error(f'Failed to update sheets for {process_name}')
                        print(f'{process_name} failed to update sheets')        



                elif privacy == 0:
                    vimeo_url = vimeo_upload(file_location + message, title_for_videos, description)
                    
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

            r.hsetnx(title,'title',title)
            r.hsetnx(title,'vimeo_url',vimeo_url)

            try:
                sub = sub_files[0]['en']
                print(sub)
                print(vimeo_url)
                subtitle_upload_response = subtitle_upload(vimeo_url,sub)


            except:

                print('Failed to upload subtitles')     

            try:
                post_to_s3(file_location,message, f'{uuid}_{title}.mp4',output_bucket)  ####CFH Need to fix this This needs to be changed for the input files
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
                file_locations = [file_location, './']
                clean_up(file_locations, key)
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


            try:   
                s3_link_public = f'https://s3-eu-west-1.amazonaws.com/{output_bucket}/{uuid}_{title}.mp4'
                message_attributes = processing_output_message(youtube_url, s3_link_public, uuid, vimeo_url)
                sqs = boto3.resource('sqs',region_name='eu-west-1')
                youtube_queue = sqs.get_queue_by_name(QueueName='Talkbot_output')
                data = {}
                data['Body'] = message_attributes
                data = json.dumps(data)
                youtube_queue.send_message(MessageBody=data, MessageAttributes=message_attributes)


                try:
                    r.hset(key,'status','Avenger queue populated')                    
                    r.hset(key,'s3_link_public',s3_link_public)


                except Exception as e:
                    logging.error(f'{process_name} failed to update sheets')
                    print(f'{process_name} failed to update sheets')



            except Exception  as e:
                print('Failed to populate avenger queue')
                logging.error(f'Failed to populate avenger queue for {message}')

            try: 

                message_attributes = processing_output_babble(s3_link_public, uuid, vimeo_url,speakers,sub_files[3], title)
                print(message_attributes)
                sqs = boto3.resource('sqs',region_name='eu-west-1')
                youtube_queue = sqs.get_queue_by_name(QueueName='Babble')
                data = {}
                data['Body'] = message_attributes
                data = json.dumps(data)
                youtube_queue.send_message(MessageBody=data, MessageAttributes=message_attributes)



            except Exception  as e:
                print('Failed to populate Babble queue')
                logging.error(f'Failed to populate Babble queue for {message}')                


          


            print(f'{process_name} process finishes {message}')

            
            try:
                r.hset(key,'status','Finished')

            except Exception as e:
                logging.error(f'{process_name} failed to update sheets')
                print(f'{process_name} failed to update sheets')



    return




def main(input_bucket, output_bucket,free_cores= 0, priority_cores = 1):
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

    logger = logging.getLogger(__name__)
    tasks_normal = multiprocessing.Queue(-1) 
    tasks_priority = multiprocessing.Queue(-1)


    logging_queue = multiprocessing.Queue(-1)
    
    
    listener = multiprocessing.Process(target=listener_process,
                                       args=(logging_queue, listener_configurer))

    listener.start()

    num_processes = multiprocessing.cpu_count() - free_cores - priority_cores 

    for i in range(num_processes):
        process_name = 'Ordinary_{}'.format(str(i))


        new_process = multiprocessing.Process(name = process_name ,target=processing_message, args=(logging_queue, worker_configurer,
        process_name, tasks_normal,input_bucket, output_bucket))

        new_process.start()


    for i in range(priority_cores):

        process_name = 'Priority_{}'.format(str(i))

        new_process = multiprocessing.Process(name = process_name, target=processing_message, args=(logging_queue, worker_configurer,
        process_name, tasks_priority,input_bucket, output_bucket))

        new_process.start()    



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
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            messages.append(temp)

        for message in messages:
            print(message) 

            try:
                message = message.lstrip(input_bucket + '/') 
                #uuid = message.split('_')[-3]
                uuid = 'blank' 
                keys = r.keys()
                keys = [c for c in keys if uuid in c]

                if len(keys) != 1:
                    raise Exception('No single key found')
                    logger.exception(f'Failed to find unique key for{uuid}')
                    continue
                else:
                    key = keys[0]

                print(key)

            except Exception as e:
                logger.exception(f'Failed to find unique key for {uuid}')        

            try:
                r.hset(key,'status','UUID processed')

            except Exception as e:
                    logger.exception(f'Failed to updated Redis for {uuid}; Processing')


            try:
                block = int(r.hget(key,'block'))
                print('Block')
                if block == 1:
                    print(f'{uuid} has been blocked')  
                    continue

                else: 
                    pass
            
            except Exception as e:
                logger.exception(f'Failed to read block status for {uuid}')

            try:
                priority = int(r.hget(key,'priority'))
                print('priority')


                if priority == 1:
                    tasks_priority.put([key,uuid,message])

                elif priority == 0:
                    tasks_normal.put([key,uuid,message])

            except Exception as e:
                logger.exception(f'Failed to read priority status for {uuid}')            

        time.sleep(5)



if __name__ == '__main__':
    input_bucket = 'cfh-input'
    output_bucket = 'cfh-output'
    file_location = '/home/ubuntu/AJM/video_files/'
    
    

    main(input_bucket = input_bucket, output_bucket = output_bucket)