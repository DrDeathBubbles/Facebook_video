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
#sys.path.append('./youtube/')

from video_upload import youtube_video_upload, processing_youtube_url

sys.path.append('./logging/')

from queuehandler import QueueHandler

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
#from People_processing import *
from Email_processing import *
from People_processing_CC import *

import Schedule as sch

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
    #h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    h = QueueHandler(queue)  # Just the one handler needed
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

def processing_message(queue, configure, process_name, tasks, results, speaker_email_data, sting, watermark, slug, sheet_id, sheet_name):
    """
    Processes the message which is sent 
    """
    while True:
        task = tasks.get()
        message = task[0]
        configure(queue)
        logger = logging.getLogger('main_logger')
        level = logging.INFO

        schedule = sch.get_spreadsheet(sheet_name)



        if message == 0:
            print('{} process quits'.format(process_name))
        else:
            print('{} recieved {}'.format(process_name,message))


            try:
                uuid = message.split('_')[-3]
                row = sch.find_row(schedule,'id',uuid) + 2
                
            except Exception as e:
                logger.log(logging.Error, 'Failed to find uuid in schedule for {}'.format(message))
                print('Failed to find uuid in schedule for {}'.format(message))


            try:
                cell_range = 'I{0}:I{0}'.format(row)
                flag = sch.read_single_range(sheet_id, cell_range)
                flag = flag['values'][0][0]

                if 'values' in flag.keys():

                    try:
                        cell_range = 'K{0}:K{0}'.format(row)
                        sch.write_single_range(sheet_id, cell_range,[['Upload Blocked']])

                    except Excpetion as e:
                        logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                        print('{} failed to update sheets'.format(process_name))

                    continue

            except Excpetion as e:
                logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                print('{} failed to update sheets'.format(process_name))





            try:
                avenger = avenger_requests.avenger_requests(slug)
                talk_location_id = avenger.get_timeslot_id(uuid)

                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Processed Avenger ID']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))

            except Exception as e:
                logger.log(logging.ERROR,'Avenger lookup failed for {}'.format(message))
                print('Avenger lookup failed for {}'.format(message))

                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Failed to process Avenger ID']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))

                continue


            try:
                retrieve_from_s3(message)
                print('{} retrieves from S3'.format(process_name))
                
                
                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Retrieved video from S3']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))


            except Exception as e:
               logger.log(logging.ERROR,'Problem retrieving {}'.format(message))
               print('Problem retrieving {}'.format(message))

                
               try:
                   cell_range = 'K{0}:K{0}'.format(row)
                   sch.write_single_range(sheet_id, cell_range,[['Failed to retrieve video from S3']])

               except Excpetion as e:
                   logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                   print('{} failed to update sheets'.format(process_name))

               continue 



            try:
                video_processing(process_name,file_location+message, sting, watermark, file_location +'edited_videos/'+message)
                print('Video processing successful')
                
                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Video processed']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))



            except Exception as e:
                logger.log(logging.ERROR,'Problem processing {}'.format(message))
                print('Problem processing {}'.format(message))
                os.rename(file_location+message,file_location +'edited_videos/'+message)

                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Failed to process video']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))
            
            
            
            print('{} processed video'.format(process_name))           


            #This is where we process the message and get information regarding the fb_page_id
            # and the access_token needed for the rest of the upload 


            try:
                description = avenger.description_processing(uuid)
                speakers = avenger.name_processing(uuid)
                speakers_for_emails = avenger.speaker_names(uuid)
                title = avenger.title_processing(uuid)
                title = string_processing(title) 
                description = speakers + ' \n ' + description

                
                
                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Metadata acquired']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))
            
            
            except Exception  as e:
                print('Failed to obtain metadata')
                logger.log(logging.ERROR, 'Failed to obtain metadata {}'.format(message))
                logging.error(e)
            

                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Failed to obtain metadata']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))

            try:
                #youtube_post = youtube_video_upload(file_location + 'edited_videos/' + message, title, description,'WebSummit','22','private')
                youtube_post = youtube_video_upload(file= file_location + 'edited_videos/' + message,title= title, description=description,keywords='AJM F',category='22',privacyStatus='private') 


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Posted to youtube']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))

                youtube_url = processing_youtube_url(youtube_post) 

                try:
                    cell_range = 'M{0}:M{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[[youtube_url]])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))
 





            except:
                logger.log(logging.ERROR,'Failed to post to youtube {}'.format(message))
                print('Failed to post to Youtube')


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Failed to post to youtube']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))


                continue
            
            #This is where we get the description and speakers for a talk and add
            # it to the facebook video            
            

            try: 
                post_to_s3(file_location,message, uuid + '_' + title)
                print('Successfully posted to S3') 
                
                
                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Posted to s3']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))
          
          
            except Exception as e:
                logger.log(logging.ERROR,'Failed to post to S3 {}'.format(message))
                print('Failed to upload video to S3')


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Failed to post to s3']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))




            try:
                os.remove(file_location + message)
                os.remove(file_location + 'edited_videos/' + message)
                print('removed local files')


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Removed local files']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))



            except:
                logger.log(logging.ERROR,'Failed to delete the local copy of the file {}'.format(message))
                print('Failed to remove local copies')


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Failed to remove local fires']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))


            #This is where we get the video url for the facebook video and email it
            #to the speakers

            try:   
                youtube_url = processing_youtube_url(youtube_post) 
                print(youtube_url)
                s3_url = 'https://s3-eu-west-1.amazonaws.com/ws18-videos/' + uuid + '_' + title   
                message_attributes = processing_output_message(youtube_url, s3_url, uuid)
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


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Avenger queue populated']])
                    cell_range = 'N{0}:N{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[[s3_url]]) 

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))



            except Exception  as e:
                print('Failed to email speakers')
                logger.log(logging.ERROR, 'Failed to email speakers for {}'.format(message))
                logging.error(e)


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Avenger queue failed to populate']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))


            time.sleep(10)
            try:
                for speaker in speakers_for_emails:
                    emails = get_emails_cc(speaker, speaker_email_data)
                    send_email(emails[0],emails[1],youtube_url) 
                    time.sleep(5)


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Speakers emailed']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))

            except:
                print('Emails have not been sent!')    
                logger.log(logging.ERROR, 'failed to cc email {}'.format(message))


                try:
                    cell_range = 'K{0}:K{0}'.format(row)
                    sch.write_single_range(sheet_id, cell_range,[['Speakers not emailed']])

                except Excpetion as e:
                    logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                    print('{} failed to update sheets'.format(process_name))

            print('{} process finishes {}'.format(process_name, message))

            
            try:
                cell_range = 'K{0}:K{0}'.format(row)
                sch.write_single_range(sheet_id, cell_range,[['FINISHED']])

            except Excpetion as e:
                logging.log(logging.Error, '{} failed to update sheets'.format(process_name))
                print('{} failed to update sheets'.format(process_name))



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

        new_process = multiprocessing.Process(target=processing_message, args=(queue, worker_configurer, process_name, tasks, results, speaker_email_data, sting, watermark,slug, sheet_id, sheet_name))

        new_process.start()


#Setting up the connection to monitor SQS 

    #conn = initialise_connection()
    #q = conn.create_queue('DS_AJM_VIDEO')
    sqs = boto3.resource('sqs',region_name = 'eu-west-1')
    q = sqs.get_queue_by_name(QueueName='DS_AJM_VIDEO')    



    while True:

        messages = []
        #rs = q.get_messages()
        rs = q.receive_messages()
        for m in rs:
            #temp = json.loads(m.get_body())
            temp = json.loads(m.body)
            m.delete()
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
        slug = 'ws18'

    elif presets == 1:
        speaker_email_data = input('Enter the full string path for the speaker email list:')
        sting = input('Enter the full string path for the sting:')
        watermark = input('Enter the full string path for the watermark:')

    else:
        print('Error - must enter eithe DEFAULTS or INPUTS')        
        exit()

    main(speaker_email_data,slug=slug)