import requests
import os 
access_token = os.environ['ACCESSTOKEN_VIDEO_2']

def upload_video(video_path):
    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file) 
    return flag


def adding_description(post_id,description):
    data = {'description':description}
    url = 'https://graph.facebook.com/v2.10/{}?access_token={}'.format(post_id,access_token)
    flag = requests.post(url,json=data)
    return flag
    #4244502276763251

def reading_video_url(post_id):
    url = 'https://graph.facebook.com/v2.10/{}?fields=permalink_url&access_token={}'.format(post_id,access_token)
    flag = requests.post(url)
    return flag