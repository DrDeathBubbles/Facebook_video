import requests
import os 
access_token = os.environ['ACCESSTOKEN_VIDEO_2']





def upload_video(video_path):
    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token_2) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file) 
    return flag


def adding_description(post_id,description):
    data = {'description':description}
    url = 'https://graph.facebook.com/v2.10/{}?access_token={}'.format(post_id,access_token)
    flag = requests.post(url,json=data)
    return flag
    #1424450227676325