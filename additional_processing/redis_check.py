import redis 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd  

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
    s3_resource.Object('ds-ajm-videos', file_name).copy(copy_source)


from boto3 import client

bucket_keys = []
conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
for key in conn.list_objects(Bucket='ds-ajm-videos')['Contents']:
    bucket_keys.append(key['Key'])


#copy_to_bucket('ds-ajm-videos', 'ds-ajm-videos', )


r = redis.Redis(host='localhost', port = 6379, db=0)

keys = r.keys()
not_processed = []
not_processed_at_all = []


for key in keys:
    if r.hexists(key,'s3_url_video') is False and r.hget(key,'status') == b'Finished' :
        not_processed.append(key)


for key in keys:
    if r.hget(key,'status') == b'Unprocessed' :
        not_processed_at_all.append(key)        


df = []
for key in not_processed:
    df.append(r.hgetall(key))

unprocessed_keys = [i[b'id'].decode('utf-8') for i in df]







bucket_keys = []
client = boto3.client('s3')
paginator = client.get_paginator('list_objects')
page_iterator = paginator.paginate(Bucket='ds-ajm-videos')
for page in page_iterator:
    bucket_keys.append(page['Contents'])

total_bucket_keys  = bucket_keys[0] + bucket_keys[1] + bucket_keys[2]
total_bucket_keys = [i['Key'] for i in total_bucket_keys]
total_bucket_keys = pd.DataFrame(total_bucket_keys)
total_bucket_keys.columns = ['Keys']




for key in unprocessed_keys[1:]:
    location = total_bucket_keys['Keys'].apply(fuzzy_matching,file_title=key)
    location = location.idxmax()
    file_name = total_bucket_keys.ix[location]['Keys']
    print(f'{key} links to {file_name}')
    copy_to_bucket(file_name)


