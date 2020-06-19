import glog
import boto3




file_location =  '/Volumes/My Passport/CFH/Channel 1'
s3 = boto3.resource('s3')
output_bucket = 'cfh-input'

def post_to_s3(input_file_name, output_file_name, output_bucket):
    my_bucket = s3.Bucket(output_bucket)
    a = my_bucket.upload_file(input_file_name, output_file_name)
    return 


files = glob.glob('*.mp4')


for f in files:
    post_to_s3(f,f.replace(' ','_'), output_bucket )
    print(f.replace(' ','_'))
