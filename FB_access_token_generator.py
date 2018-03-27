import requests
import os

def video_info():
    url = 'https://graph.facebook.com/v2.10/1414598331994848?access_token={}'.format(os.environ['ACCESSTOKEN'])

    flag = requests.get(url)
    return flag


def managed_pages(access_token):
    """
    Gives a list of the pages which are managed by our access token and the access token associated with these pages
    """
    url = 'https://graph.facebook.com/me/accounts?access_token={}'.format(access_token)
    flag = requests.get(url)
    return flag

def get_short_term_token():
    """
    Don't know what this is 
    """

    url = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(os.environ['APPID'],os.environ['APPSECRET'])

    flag = requests.get(url)

    return flag


def get_long_lasting_token(short_term_token, client_id, client_secret):
    """
    From a short term page access token get the long term page access token
    """
    url = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=fb_exchange_token&fb_exchange_token={}'.format(client_id, client_secret, short_term_token)

    flag = requests.get(url)

    return flag


def get_long_lasting_token_return(short_term_token, client_id =os.environ['APPID_EXPERIMENTS_TEST'], client_secret=os.environ['APPSECRET_EXPERIMENTS_TEST']):
    """
    From a short term page access token get the long term page access token
    """
    url = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=fb_exchange_token&fb_exchange_token={}'.format(client_id, client_secret, short_term_token)

    flag = requests.get(url)
    if 'access_token' in flag.json().keys():
        flag = flag.json()['access_token']
        return flag
    else:
        return None


#def long_lasting_token():
#    access_token= 'EAAXukhZA5tLEBAE3LQomvcItWAGzQ4hOllmusAvb8R4Q3aISRxEc0nx4zZAz7rAjXpodx8jJHqZCJQWZCg238geZA9GD4XZB0CSZCXTONm7hBdZAWlMlhrXjEI4AtGFvaTz2OBqlFyi1nGg7HNlxrmVsDCAFgIpAnucAJPd9v3OX547JMmfG967iqUdF1C58HuMZD'
#    url = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=fb_exchange_token&fb_exchange_token={}'.format(os.environ['APPID'],os.environ['APPSECRET'],access_token)
#
#    flag = requests.get(url)
#
#    return flag


def long_lasting_token_2():
    access_token= 'EAAXukhZA5tLEBACXIaGKSlzo8FZBW1sA9PZAuZAXpxzYUJHMu0KddsKvamTG7F3l5gzjZB82UbShnC04d9a90IbTfVAhhIhJOYcmMBVpNxfZATbSZAMNLRsNC9Tv81qJab5AKtkxpKhdONwGrRyOgJ5zofUhajooZC6m0KHCEZCMh1brnRWbiV2fSoZBAo6M7ee8oZD'
    url = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=fb_exchange_token&fb_exchange_token={}'.format(os.environ['APPID_EXPERIMENTS'],os.environ['APPSECRET_EXPERIMENTS'],access_token)

    flag = requests.get(url)

    return flag



access_token = 'EAAXukhZA5tLEBAOJ4EYUzZAQxazrHNfRZCe2iIDRCJ3T2dRvv6eZCN4QZAFXZAGAvhtktz0fKOznN9nIFkHE7EfWnpkgtFjlZCwIA1MFkIWkIIhYeQgHSORrRVRq9slf0v0AbyZC70si8nk4djYmVeMKbrSaMJ9mRoLmIPa012gNl2V3WvJKvPeZCPpAp0TCAk0UZD'
access_token_2 = 'EAAXukhZA5tLEBAHugzUifhrugnWeTrgvtJiInUbFUSyUp1t6AOPc8ZCFUv1o1c0ZBJcnZBzkdOW1MvfcZCPDswXAvEtZAu8mzQ5bT5NbMenImBzwMauDgbcSUjZBWHvK6Hr7zNTU60CfZCZABNzEfeMd5ZCyq14iIE3iBI0ZBPvfnw2ZAgZDZD'
def upload_video(video_path):
    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token_2) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file) 
    return flag

def upload_video_2(video_path,access_token):
    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file) 
    return flag

def upload_video_3(video_path,access_token):
    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file) 
    return flag


if __name__ == '__main__':
    a = managed_pages(os.environ['ACCESSTOKEN'])
    access_token = a.json()['data'][0]['access_token']
    out = upload_video_2('./test_trimmed.mp4',access_token)
    print(out.text)