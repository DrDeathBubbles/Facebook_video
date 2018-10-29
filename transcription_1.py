from __future__ import print_function
import time
import boto3
import nltk
import requests
import string 
import collections
import json
import os
from textblob import TextBlob
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from textblob import Word
from time import sleep
from rake_nltk import Rake 


def aws_transcribe(job_name,job_uri):
    transcribe = boto3.client('transcribe', region_name = 'eu-west-1')
    job_uri = "https://s3-eu-west-1.amazonaws.com/cc18-videos/CC18_audio/09713108-36c7-4232-bde7-2a2ece553088_The_sole_obligation_of_a_firm_is_to_create_wealth_for_its_shareholders.mp3"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    return status



def get_text(response):
    trans_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    text = requests.get(trans_url)
    text = text.json()
    text = text['results']['transcripts']
    text = text[0]['transcript']
    return text 


def get_messages():
    sqs = boto3.resource('sqs',region_name = 'eu-west-1')
    queue = sqs.get_queue_by_name(QueueName='Talkbot_transcription')
    out = []
    for message in queue.receive_messages():
        out.append(json.loads(message.body)['Body'])
        queue.delete_message(message)
    return out 

def save_text_to_s3(uuid, text):
    file_name = uuid + '.txt' 
    with open(file_name,'w') as f:
        f.write(text)

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('ws18-videos')    
    a = my_bucket.upload_file(file_name, 'transcriptions/'+file_name)
    os.remove(file_name)
    return a

def key_word_analysis(text):
    r = Rake(min_length=2, max_length=4)
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    return keywords 





def main():
    while True:
        messages = get_messages()
        for message in messages:
            s3_url, uuid = message[0]['s3_url'], message[0]['uuid']
            response = aws_transcribe(uuid, s3_url)
            text = get_text(response)
            save_text_to_s3(uuid, text)
            keywords = key_word_analysis(text)






        sleep(60*5)
    
    








