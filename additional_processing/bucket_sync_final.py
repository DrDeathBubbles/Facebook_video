import redis 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd  
from datetime import datetime
import boto3 
s3_resource = boto3.resource('s3')



def fuzzy_matching(talk_title, file_title):
    """
    Fuzzy matching taking the talk title as the input
    And the field_title as the title which is supplied
    """
    return fuzz.ratio(talk_title, file_title)



def copy_to_bucket(file_name):
    copy_source = {
        'Bucket': 'ds-ajm-videos',
        'Key': file_name
    }
    s3_resource.Object('ds-ajm-videos/', 'vimeo_cc19/' +file_name).copy(copy_source)


def total_bucket_keys(bucket_name):
    bucket_keys = []
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket_name)
    for page in page_iterator:
       bucket_keys.append(page['Contents'])    
    total_bucket_keys = [item for sublist in bucket_keys for item in sublist]
    return total_bucket_keys

def get_conference(objs, start_date, end_date):
    out = []
    for obj in objs:
        if (start_date < obj['LastModified'].date()) & (end_date > obj['LastModified'].date()):
            out.append(obj)
    return out

if __name__ = '__main__':
    start_date = start_date = datetime(2019,5,20)
    start_date = start_date.date()

    end_date = datetime(2019,6,17)
    end_date = end_date.date()

    bucket_keys = total_bucket_keys('ds-ajm-videos')
    conference = get_conference(bucket_keys,start_date,end_date)