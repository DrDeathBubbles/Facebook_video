import boto3
import botocore

BUCKET_NAME = 'ds.aj.videos' # replace with your bucket name
KEY = 'test_trimmed_7.mp4' # replace with your object key

keys = []

s3 = boto3.resource('s3')

my_bucket = s3.Bucket('ds.ajm.videos')
for objects in my_bucket.objects.all():
    keys.append(objects.key)

a = my_bucket.download_file(keys[2],keys[2])

#try:
#    s3.Bucket(BUCKET_NAME).download_file(KEY, 'downloaded_file.mp4')
#except botocore.exceptions.ClientError as e:
#    if e.response['Error']['Code'] == "404":
#        print("The object does not exist.")
#    else:
#        raise