import boto3
import re
import sys
import pandas as pd
import os
sys.path.append('./additional_processing/')
from vimeo_library import *

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
file_location = '/home/ubuntu/AJM/video_files/'

def copy_file(key):
    source= { 'Bucket' : 'ws20-broadcast-raw', 'Key': f'{key}'}
    dest = s3.Bucket('ws20-input')
    dest.copy(source, f'{key}')

def download_file(key):
    s3_client.download_file('ws20-output', key, file_location + key)    


def uuid_get(x):
    out = re.findall(r'\d{9}', x)
    if len(out) > 0:
        return int(out[0])
    else:
        return 0    

def get_bucket_data(bucket_name):
    my_bucket = s3.Bucket(bucket_name)
    content = []
    for my_bucket_object in my_bucket.objects.all():
        content.append(my_bucket_object.key)
    content_pd = pd.DataFrame(content)
    content_pd.columns = ['Key']
    content_pd['UUID'] = content_pd['Key'].apply(uuid_get)
    content_pd['UUID'] = content_pd['UUID'].astype('int64')
    return content_pd


if __name__ == '__main__':
    b_output = 'ws20-output'
    processed_vimeo = pd.read_csv('WS20_vimeo_links.csv')
    processed_vimeo_uuids = processed_vimeo['Monday ID'].to_list()

    lookup_data = pd.read_csv('./WS20_data/finally_merged_data.csv')
    new_lookup_data = lookup_data.drop_duplicates(subset = 'FILE NAME')

    output_pd = get_bucket_data(b_output)

    to_be_processed = output_pd[~output_pd['UUID'].isin(processed_vimeo_uuids)]

    for row in to_be_processed[0:5].iterrows():
        key = row[1]['Key']
        uuid = uuid_get(key)
        match = new_lookup_data[new_lookup_data['UUID'] == uuid]
        if len(match) == 1:
            title = match['Talk Title'].values[0]
            description = match['Description'].values[0]
            download_file(key)
            vimeo_url = vimeo_upload(file_location + key, title, description, privacy = 'unlisted')
            with open(f'/home/ubuntu/Talkbot/Facebook_video/output_data/data_{uuid}.csv','a') as f:
                f.write(f"{uuid},{title},{vimeo_url}")
            os.remove(file_location + key)