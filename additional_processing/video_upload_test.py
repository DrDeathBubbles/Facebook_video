import pandas as pd
import avenger_requests
import requests
import logging


def upload_video(video_path, fb_page_id, access_token):
    """
    Returns {'id': '1450967228357958'}
    """
    url = 'https://graph-video.facebook.com/{}/videos?access_token={}'.format(fb_page_id, access_token) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file)
    try:
        flag.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Http error {}'.format(err)) 
        raise Exception
    return flag



if __name__ == '__main__':

    message = 'CS_8_02_09cb8167-6a3c-4817-bc4e-976ed4f0edeb_000000_000018.mp4'

    try:
        data = pd.read_csv('CC_18_access_tokens.csv')
        uuid = message.split('_')[3]
        avenger = avenger_requests.avenger_requests()
        talk_location_id = avenger.get_timeslot_id(uuid)
        fb_page_id = int(data[data['id']==talk_location_id]['page_id'])
        access_token = data[data['id']==talk_location_id]['long_lasting_token'].values[0]
        print('Got')
    
    except Exception as e:
        logging.error('Failed to get the credentials')
        print('Failed to get credentials')    

    try:
        post = upload_video('./CS_8_02_09cb8167-6a3c-4817-bc4e-976ed4f0edeb_000000_000018.mp4', fb_page_id, access_token)
        print('Posted to facebook') 

    except:
        print('Post to facebook unsuccessful')




