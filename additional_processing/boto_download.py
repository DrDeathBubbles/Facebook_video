import boto3
import botocore

BUCKET_NAME = 'ds.aj.videos' # replace with your bucket name
KEY = 'test_trimmed_7.mp4' # replace with your object key

keys = []

s3 = boto3.resource('s3')

my_bucket = s3.Bucket('ds.ajm.videos')
for objects in my_bucket.objects.all():
    keys.append(objects.key)

a = my_bucket.download_file(keys[3],keys[3])



bucket_name = 'ds.ajm.videos'
path_to_videos = "/Users/aaronmeagher/AJM/video_files/"
path_to_videos = '/home/ubuntu/AJM/video_files'
s3 = boto3.resource('s3')

def retrieve_from_s3(filename):
    my_bucket = s3.Bucket('ds.ajm.videos')
    a = my_bucket.download_file(filename,path_to_videos + filename)
    return a