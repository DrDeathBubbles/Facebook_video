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


def get_file_list_url(s3_bucket_name):
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(s3_bucket_name)
    get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))
    unsorted = []
    for file in my_bucket.objects.filter():
        unsorted.append(file)
    files = [obj.key for obj in sorted(unsorted, key=get_last_modified, reverse=True)][1:]
    files_url = ['https://s3-eu-west-1.amazonaws.com/' + s3_bucket_name + '/' + f for f in files]
    return list(zip(*[files,files_url])) 



if __name__ == '__main__':
    files = get_file_list_url(ws18_audio)
    for f in files:
        job = aws_transcribe(f[0],f[1])
        text = get_text(job)
        file_name = f[0].rstrip('.mp3') + '.txt'
        with open('./transcription/' + file_name,'w') as f:
            f.write(text)