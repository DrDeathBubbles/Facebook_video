import requests
import os
import boto3
import pandas as pd

s3 = boto3.resource('s3')
token = 'fio-u-mTMmGXevbXIDnTsFlGmC2MQgTvISaSQfLZPrQzI_nKwwB0tfEfZfTJkHDQ3Nzf-C'
token = 'fio-u-g5Ls98NOufRLocdaXKNHOIYUZDwkJrGh7Uv9-7wHPS67J-Fn_E7hiRlbpKV6d9c0'
account_id_team = '27c611aa-21bd-4952-905a-7d7749140bb4'
websummit_id = '27c611aa-21bd-4952-905a-7d7749140bb4'
my_bucket = 'ws20-input' 
headers = headers_id = {"Accept": "application/json","Authorization": f"Bearer {token}"} 



def download_file(download_url, download_name, download_folder):
    file_download = requests.get(url = download_url)
    with open(download_folder + download_name, 'wb') as f:
        f.write(file_download.content)

def save_asset_to_s3(download_url, file_name):
    file_download = requests.get(url = download_url)
    client = boto3.client('s3')
    client.put_object(Body=file_download.content, Bucket=my_bucket, Key=file_name)
    print(f'{file_name} is finished')



def team_accounts():
    team_accounts = f"https://api.frame.io/v2/accounts/{account_id_team}/teams"
    request = requests.get(team_accounts, headers = headers)

def walk_data(json_object):
    data = []
    for i in json_object:
        if i['project']['name'] == 'YAL Ingest - NO Touch':
            if 'original' in i.keys():
                data.append({'file_name':i['name'], 'id':i['id'], 'download_link':i['original'],'project_name': i['project']['name']})
    return(data)

def frameio_content():
    
    data = {
    "account_id":f"{websummit_id}",
    "q": "",
    "sort": "name",
    "page_size": 100,
    'page':1
    }

    out_data = []
    search = requests.post('https://api.frame.io/v2/search/library', data = data, headers = headers)
    max_page = int(search.links['last']['url'].split('=')[1])
    for i in range(1, max_page + 1):
        data = {
         "account_id":f"{websummit_id}",
         "q": "",
         "sort": "name",
         "page_size": 100,
         'page':i
         } 
        search = requests.post('https://api.frame.io/v2/search/library', data = data, headers = headers)
        out_data = out_data + walk_data(search.json()) 

    return out_data    

def extract_uuid_from_filename(filename):
    temp = filename.split('_')
    out = 0 
    for t in temp:
        if len(t) == 9 and t.isnumeric():
            out = t
    return out



def make_data_frame(data):
    mark_data =pd.read_csv('./WS20_data/WS20_data_mark.csv')
    frame_io_data = frameio_content()
    frame_io_data = pd.DataFrame(frame_io_data)
    frame_io_data['UUID'] = frame_io_data['file_name'].apply(extract_uuid_from_filename)
    frame_io_data['UUID'] = frame_io_data['UUID'].astype('int64')
    data_merge = pd.merge(mark_data,frame_io_data, on = 'UUID') 
    

def extract_data(data,uuid):
    temp = data[data['UUID'] == uuid]
    temp = temp[temp['file_name_2'].str.contains('FIN')]
    download_url = temp['download_link'].values[0]
    file_name = temp['file_name_2'].values[0]
    return [download_url, file_name] 

if __name__ == '__main__':
    data = pd.read_csv('WS20_data/finally_merged_data.csv')
    data['file_name_2'] = data['file_name'].str.replace(' ','_')
    data[['download_link','file_name_2']][0:50].apply(lambda x: save_asset_to_s3(x['download_link'],x['file_name_2']), axis = 1)
    #speaker_schedule = pd.read_csv('./WS20_data_Speaker_Schedule.csv')
    #frame_io_data = pd.DataFrame(frameio_content())
    #merged_data = pd.merge(frame_io_data, speaker_schedule, left_on='monday_uuid', right_on='UUID')


#account_id = 'f7bb64c1-1bd2-4229-b4cd-e70b02c10502'
#account_id_team = '27c611aa-21bd-4952-905a-7d7749140bb4'