import glob

def uuid_get(x):
    out = re.findall(r'\d{9}', x)
    if len(out) > 0:
        return out[0]
    else:
        return 0  

path ='/home/ubuntu/AJM/video_files/edited_videos/masterclasses_live_final_2/' 
files = glob.glob(path + '*.mp4' )
bucket = 'ws20-output'
my_bucket = s3.Bucket('ws20-output')
for f in files:
    file_name = f.lstrip(path)
    uuid = uuid_get(file_name)
    link = f'https://s3-eu-west-1.amazonaws.com/{bucket}/{file_name}'
    my_bucket.upload_file(f,file_name)
    with open('live_masterclasses_file_links.csv','a') as a:
        a.write(f'{uuid},{link}\n')


retries_samsung = ['WS20_72_780050398_PTH_MTC.mp4']
retries = ['WS20_81_780050485_PTH_MTC-029.mp4','WS20_86_780050504_PTH_MTC-023.mp4','WS20_135_858027876_PTH_MTC.mp4',]
retries = ['WS20_90_780050493_PTH_MTC.mp4']
retries=['C31.2_WS20_719722367_TLK_EDT_V1_FIN.mp4']
file_location = '/home/ubuntu/AJM/video_files/'
input_bucket = 'ws20-input'
bucket = 'ws20-output'
my_bucket = s3.Bucket('ws20-output')
for r in retries:
    uuid = uuid_get(r)
    retrieve_from_s3(r, input_bucket)
    file_name = 'manual_' + r
    final_file_location = '/home/ubuntu/AJM/video_files/masterclass_final_thursday/' + file_name
    video_processing_WS20('0',file_location + r,watermark, final_file_location)
    my_bucket.upload_file(final_file_location, file_name) 
    link = f'https://s3-eu-west-1.amazonaws.com/{bucket}/{file_name}'
    with open('live_masterclasses_file_links_monday.csv','a') as a:
        a.write(f'{uuid},{link}\n')
