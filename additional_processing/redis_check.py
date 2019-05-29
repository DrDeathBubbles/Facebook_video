import redis 


import boto3 
s3_resource = boto3.resource('s3')


def copy_to_bucket(file_name):
    copy_source = {
        'Bucket': 'ds-ajm-videos',
        'Key': file_name
    }
    s3_resource.Object('ds-ajm-videos', 'ds-ajm-videos').copy(copy_source)



copy_to_bucket('ds-ajm-videos', 'ds-ajm-videos', )


r = redis.Redis(host='localhost', port = 6379, db=0)

keys = r.keys()
not_processed = []



for key in keys:
    if r.hexists(key,'s3_url_video') is False:
        not_processed.append(key)


df = []
for key in not_processed:
    df.append(r.hgetall(key))






