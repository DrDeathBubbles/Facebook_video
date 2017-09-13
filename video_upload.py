# A python programme for the uploading of videos to facebook
import requests
import os

url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(os.environ['ACCESSTOKEN'])
video_path ='/Users/aaronmeagher/Desktop/test_trimmed.mp4'
files = {'file':open(video_path,'rb')}
flag = requests.post(url,files=files)
