import boto3 
from datetime import datetime
import pandas as pd

end_of_conference = datetime(2018,11,11).date()
start_of_conference = datetime(2018,11,4).date()


def conference_videos(bucket, start_date, end_date):

    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))


    s3 = boto3.client('s3')
    objs = s3.list_objects_v2(Bucket=bucket)['Contents']
    [obj['Key'] for obj in sorted(objs, key=get_last_modified)]


    for obj in objs:
        obj['LastModified'] = obj['LastModified'].date()

    df = pd.DataFrame(objs)

    df =  df[(start_of_conference < df['LastModified']) & (df['LastModified'] < end_of_conference) ]

    return df 

    


df_source = conference_videos('ds-ajm-videos', start_of_conference, end_of_conference)
new = df_source['Key'].str.split('_', expand = True)
df_source['uuid'] = new[3]


df_desdination = conference_videos('ws18-videos', start_of_conference, end_of_conference)
new = df_desdination['Key'].str.split('_', expand = True)
df_desdination['uuid'] = new[0]


