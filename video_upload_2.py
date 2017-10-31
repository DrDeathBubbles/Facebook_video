import requests
import os 
access_token = os.environ['ACCESSTOKEN_VIDEO_2']
access_token = 'EAACEdEose0cBADejnZAydvACpx9dX8kZCZCWdh2Nfb5OW0e6AZCHKmZA7UsicIOee3ffDRTrq0xI2ZBnfouw1wpQgLSgBloglZCoNZCwdyZAcTrMLu1dI3xe6L2OgZClNcLS1Dpug1kjwSAAKuyrvfgsGJUkEuacoZAZAcZA4doZBsTGdYT7evj95ZAN8RxSsgJav5JlP1w3UQxaoVBZAgZDZD'
access_token ='EAAXukhZA5tLEBANmp8efbQc6ZBJfrVOmo5R5cjkjVRFzBKKdXxRire9dB4Pz4ZCvVAphXkOCWq4xllNWwAdRTr9X6PZCPW6FPdCfZC96ipZB9sOoZCI0R4vMNZB5AiZB37IIHwfEGKVrWVG5E37GxkJicsfkNZCi9CRYkgsUZBLDQcgvd9LmV5Uee6ZCiBjM1bH7JZA5MQfPlH64TDwZDZD'
#access_token = '2222EAACEdEose0cBADejnZAydvACpx9dX8kZCZCWdh2Nfb5OW0e6AZCHKmZA7UsicIOee3ffDRTrq0xI2ZBnfouw1wpQgLSgBloglZCoNZCwdyZAcTrMLu1dI3xe6L2OgZClNcLS1Dpug1kjwSAAKuyrvfgsGJUkEuacoZAZAcZA4doZBsTGdYT7evj95ZAN8RxSsgJav5JlP1w3UQxaoVBZAgZDZD'
def upload_video(video_path):
    """
    Returns {'id': '1450967228357958'}
    """

    url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token) 
    _file = {'file':open(video_path,'rb')}
    flag = requests.post(url,files=_file) 
    return flag

def upload_video_2(video_path):
    """
    Returns {'id': '1450967228357958'}
    """

    url = 'https://graph-video.facebook.com/WebSummitHQ/videos?access_token={}'.format(access_token) 
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
    """
    Returns 
    {'id': '1450967228357958',
    'permalink_url': '/LSWSTST/videos/1450967228357958/'}
    """

    url = 'https://graph.facebook.com/v2.10/{}?fields=permalink_url&access_token={}'.format(post_id,access_token)
    flag = requests.post(url)
    
    return flag