import boto3
from datetime import datetime
import pandas as pd

start_date = datetime(2018,11,4)
start_date = start_date.date()

end_date = datetime(2018,11,12)
end_date = end_date.date()



def get_conference(bucket, start_date, end_date):
    
    s3 = boto3.client('s3')
    objs = s3.list_objects_v2(Bucket=bucket)['Contents']
    out = []
    for obj in objs:
        if (start_date < obj['LastModified'].date()) & (end_date > obj['LastModified'].date()):
            out.append(obj)
    return out


ds_ajm_videos = get_conference('ds-ajm-videos',start_date,end_date)
ds_ajm_videos = pd.DataFrame(ds_ajm_videos)
temp =  ds_ajm_videos['Key'].str.split('_', expand = True)
ds_ajm_videos['uuid'] = temp[3]
ds_ajm_videos['uuid'] = ds_ajm_videos['uuid'].str.rstrip('.mp4')
set_ds_ajm_videos = set(list(ds_ajm_videos['uuid']))

ws_18_videos = get_conference('ws18-videos',start_date,end_date)
ws_18_videos = pd.DataFrame(ws_18_videos)
temp = ws_18_videos['Key'].str.split('_', expand = True)
ws_18_videos['uuid'] = temp[0]

set_ws_18_videos = set(list(ws_18_videos['uuid']))



set_ws_18_videos.difference(set_ds_ajm_videos)