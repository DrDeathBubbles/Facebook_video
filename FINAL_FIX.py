import sys
sys.path.append('./additional_processing/')

import pandas as pd
import redis
from google_drive_downloader import GoogleDriveDownloader as gdd
import multiprocessing
from vimeo_library import *
import pickle
import os

    


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



data = links_to_be_processed[['title','description','Finished Link','uuid']].values.tolist()
saving_folder = '/home/ubuntu/AJM/video_files/'

def mp_worker(inputs):
    file_id = inputs[2].lstrip('https://drive.google.com/open?id=')
    dest_path = saving_folder +  file_id + '.mp4'
    title = inputs[0]
    description = inputs[1]
    uuid = inputs[3]

    print(title)


    gdd.download_file_from_google_drive(file_id=file_id,
                                    dest_path= dest_path)
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
    data =mp_handler()
    with open('vimeo_hack_upload.data','wb') as f:
        pickle.dump(data, f)
        
    

