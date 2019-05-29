import boto3 
s3_resource = boto3.resource('s3')


def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)



copy_to_bucket('ds-ajm-videos', 'ds-ajm-videos', )