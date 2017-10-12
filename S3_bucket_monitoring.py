"""
A script to monitor the upload of videos to the S3 bucket
"""

import boto.sqs
import os 
import logging
import boto3
import botocore
import os
import json 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/myapp.log',
                    filemode='w')



def retrieve_from_s3(filename):
    os.system('s4cmd get s3://ds.ajm.videos/{} \
    ~/Desktop/Testing_folder/{}'.format(filename,filename))


def initialise_connection():
    try:
        conn = boto.sqs.connect_to_region(
        "eu-west-1",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET_KEY'])

    except KeyError as ke:
        logging.error('A keyerror {} has occured'.format(ke))

    return conn


if __name__ == '__main__':

#Setting up the connection to monitor SQS 

conn = initialise_connection()
q = conn.create_queue('DS_AJM_VIDEO')

    while true:
        messages = []
        rs = q.get_messages()
        for m in rs:
            temp = json.loads(m)
            messages.append(m.get_body())




    conn = initialise_connection()
    q = conn.create_queue('DS_AJM_VIDEO')
    rs = q.get_messages()
    m = rs[0]
    m.get_body()




