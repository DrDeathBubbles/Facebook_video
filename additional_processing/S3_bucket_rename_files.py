import boto3 
import re
bucket = 'ws20-output'

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def generate_download(key):
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'ws20-output', 'Key': key})
    return url


content = []
for my_bucket_object in my_bucket.objects.all():
    content.append(my_bucket_object.key)

def uuid_get(x):
    out = re.findall(r'\d{9}', x)
    if len(out) > 0:
        return out[0]
    else:
        return 0    

def copy(x):
    new_key =str(x[1]) + '.mp4'
    old_key = x[0] 
    s3_client.copy_object(Bucket="ws20-output", CopySource=f"ws20-output/{old_key}", Key=new_key)
    url = generate_download(new_key)
    return url


content_pd = pd.DataFrame(content)
content_pd.columns = ['Key']

content_pd['UUID'] = content_pd['Key'].apply(uuid_get)
content_pd['UUID'] = content_pd['UUID'].astype('int64')

merged = pd.merge(content_pd, prob, on = 'UUID')



my_bucket = s3.Bucket(bucket)