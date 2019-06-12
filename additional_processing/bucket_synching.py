import boto3
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('ds-ajm-videos')

out_array = []
for object in my_bucket.objects.all():
    out_array.append(object)