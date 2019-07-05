import boto3
from datetime import datetime
import pandas as pd
import sys

sys.path.append('../')


import avenger_requests_1

avenger = avenger_requests_1.avenger_requests('ws18')

start_date = datetime(2019,1,1)
start_date = start_date.date()

end_date = datetime(2019,6,12)
end_date = end_date.date()



def get_conference(objs, start_date, end_date):
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



#difference = set_ws_18_videos.difference(set_ds_ajm_videos)
difference = set_ds_ajm_videos.difference(set_ws_18_videos)
df_difference = pd.Series(list(difference))


out = []
for row in df_difference.iteritems():
    print(row[1])
    out.append(ds_ajm_videos[ds_ajm_videos['uuid'] == row[1]]['Key'])


out_2 = []

for i in out:
    if 'item' in dir(i):
        try:
            out_2.append(i.item())
        except:
            print('Error for {}'.format(i))
            continue



s3 = boto3.resource('s3')
counter = 0
for i in out_2:
    print(counter/len(out_2)*100)
    uuid = i.split('_')[-3]
    if len(uuid) == 36:
        title = avenger.title_processing(uuid)
    else:
        title = 'no_avenger_lookup'
    title = title.replace(' ', '_')
    title = uuid + '_' + title + '.mp4' 
    source= { 'Bucket' : 'ds-ajm-videos', 'Key': '{}'.format(i)}
    dest = s3.Bucket('ws18-videos')
    dest.copy(source, 'unprocessed/{}'.format(title))
    counter = counter + 1


