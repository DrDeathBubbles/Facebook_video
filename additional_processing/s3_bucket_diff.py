import boto3
import re
import pandas as pd

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


def copy_file(key):
    source= { 'Bucket' : 'ws20-broadcast-raw', 'Key': f'{key}'}
    dest = s3.Bucket('ws20-input')
    dest.copy(source, f'{key}')

def uuid_get(x):
    out = re.findall(r'\d{9}', x)
    if len(out) > 0:
        return out[0]
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
    broadcast = 'ws20-broadcast-raw'
    b_output = 'ws20-output'
    b_input = 'ws20-input'

    broadcast_pd = get_bucket_data(broadcast)
    output_pd = get_bucket_data(b_output)

    output_uuids = output_pd['UUID'].to_list()

    broadcast_sync = broadcast_pd[~broadcast_pd['UUID'].isin(output_uuids)]
    broadcast_sync['Key'].apply(copy_file)
