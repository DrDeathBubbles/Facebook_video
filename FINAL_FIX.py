import sys
sys.path.append('./additional_processing/')
import io
import pandas as pd
import redis
from google_drive_downloader import GoogleDriveDownloader as gdd
import multiprocessing
from vimeo_library import *
import pickle
import os

import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def drive_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES,)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            
    return service        
    

 

r = redis.Redis(host='localhost', port = 6379, db=0,decode_responses=True)



df = pd.concat(pd.read_excel('CFH20_Final_Delivery.xlsx', sheet_name=None), ignore_index=True)
df['title_2'] = df["Title (55 Characters)"].str.strip().str.lower()



avenger = pd.read_csv('all_talks_from_avenger_cc20.csv')
avenger.drop_duplicates(subset = ['title'], inplace=True)
vimeo_data = pd.read_csv('Vimeo_date_filtered.csv')
vimeo_data['title'] = vimeo_data['name']

already_matched = pd.merge(avenger, vimeo_data, on = 'title')

avenger_titles = set(avenger['title'])
matched_titles = set(already_matched['title'])

to_be_uploaded = avenger_titles.difference(matched_titles)

to_be_uploaded = list(to_be_uploaded)

avenger_to_be_uploaded = avenger[avenger['title'].isin(to_be_uploaded)]


avenger_to_be_uploaded['title_2'] = avenger_to_be_uploaded['title'].str.strip().str.lower()

links_to_be_processed = pd.merge(avenger_to_be_uploaded, df, on = 'title_2')

links_to_be_processed.head()

done_keys = r.keys()
links_to_be_processed  = links_to_be_processed[~links_to_be_processed['uuid'].isin(done_keys)]
data = links_to_be_processed[['title','description','Finished Link','uuid']].values.tolist()

for i in range(0,len(data)):
    if data[i][3] == '1S4FE1C9UITAB_6yiTgm_HV6KZCV2sBd2':
        data.pop(i)

saving_folder = '/home/ubuntu/AJM/video_files/'

def mp_worker(inputs):
    file_id = inputs[2].lstrip('https://drive.google.com/open?id=')
    dest_path = saving_folder +  file_id + '.mp4'
    title = inputs[0]
    description = inputs[1]
    uuid = inputs[3]

    print(title)

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    vimeo_url = vimeo_upload(dest_path, title, description, privacy = 'unlisted')
    r.hset(uuid,'vimeo_url', vimeo_url)
    os.remove(dest_path)

    print(f'{uuid}:{vimeo_url} \n')

    return [uuid,vimeo_url]

def mp_handler():
    p = multiprocessing.Pool(7)
    a = p.map(mp_worker, data)
    return a

if __name__ == '__main__':
    drive_service = drive_service()
    data =mp_handler()
    with open('vimeo_hack_upload.data','wb') as f:
        pickle.dump(data, f)
        
    

