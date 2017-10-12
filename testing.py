# A python programme for the uploading of videos to facebook
import requests
import os
##access_token = 'EAAXukhZA5tLEBAK2EymjGe7MLvZBSRFpxA9kkn4hnbuRVkcqFpdxeZBp1V2luLQoiYne71Sl8HrZBGAqX0xvk8TqBhjZCRf0PEza0oaLISLZAZAFKsS0fozS5Qy24q5aYclfKNoxdE2I5rHE3eIFpiH8AHS5htJSqnTULyh6ZAorXaH0GsvC0qxgE5ZAz8Ulstxey8ZAzTHyIQfQZDZD'
#access_token = 'EAAXukhZA5tLEBAK2EymjGe7MLvZBSRFpxA9kkn4hnbuRVkcqFpdxeZBp1V2luLQoiYne71Sl8HrZBGAqX0xvk8TqBhjZCRf0PEza0oaLISLZAZAFKsS0fozS5Qy24q5aYclfKNoxdE2I5rHE3eIFpiH8AHS5htJSqnTULyh6ZAorXaH0GsvC0qxgE5ZAz8Ulstxey8ZAzTHyIQfQZDZD'
#access_token = 'EAAXukhZA5tLEBABzNLAEQ3xoyw6Y2AILGfZAZCxibKTdzdPN2HQM6OZBg7IWTm7Y0N3jWqUf3VvBEOxMLzLfU9uBbwjcwO1elAOupNTE340ZAH4ZAv2PZBcIJvFV3GVxK9j8VgyNi1n96q3ZCee7snrkZCDpZANn8PWpzBotit5duCIIRFJQD5skzNHau7EBCQLt0ZD'
#url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(access_token)
##url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(os.environ['ACCESSTOKEN'])
##url = 'https://graph-video.facebook.com/LSWSTST/videos?access_token={}'.format(os.environ['ACCESSTOKEN_VIDEO'])
#video_path ='/Users/aaronmeagher/Desktop/test_trimmed.mp4'
#files = {'file':open(video_path,'rb')}
#flag = requests.post(url,files=files)
#curl -i -X POST \
 #-d "description=This%20is%20a%20test%20of%20adding%20a%20description" \
 #-d "title=This%20is%20a%20test%20of%20the%20title" \
 #-d "access_token=EAACEdEose0cBAM5l7HoGB2JYN0wmDQQynyCCytrrL3ORyH2ZAcIjUZC4OmTSbi7xeF74qJ9F207HlRdnWvbxkktpf0Vhw86QbRkGkaz6gWOJwpdAPAtxs91Sy2WoNVlRuV0HRXqlVSxV2i8XxsIF1BIHe2ILGprR5ySCOmZBdQF4wiIDzoAk8KBaD09BXgZD" \
 #"https://graph.facebook.com/v2.10/1424450227676325"

#This gets the info about a particular video 
access_token = 'EAAXukhZA5tLEBAHugzUifhrugnWeTrgvtJiInUbFUSyUp1t6AOPc8ZCFUv1o1c0ZBJcnZBzkdOW1MvfcZCPDswXAvEtZAu8mzQ5bT5NbMenImBzwMauDgbcSUjZBWHvK6Hr7zNTU60CfZCZABNzEfeMd5ZCyq14iIE3iBI0ZBPvfnw2ZAgZDZD' 



def video_info():
    url = 'https://graph.facebook.com/v2.10/1414598331994848?access_token={}'.format(os.environ['ACCESSTOKEN'])

    flag = requests.get(url)
    return flag

def long_lasting_token():
    access_token= 'EAAXukhZA5tLEBAE3LQomvcItWAGzQ4hOllmusAvb8R4Q3aISRxEc0nx4zZAz7rAjXpodx8jJHqZCJQWZCg238geZA9GD4XZB0CSZCXTONm7hBdZAWlMlhrXjEI4AtGFvaTz2OBqlFyi1nGg7HNlxrmVsDCAFgIpAnucAJPd9v3OX547JMmfG967iqUdF1C58HuMZD'
    url = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=fb_exchange_token&fb_exchange_token={}'.format(os.environ['APPID'],os.environ['APPSECRET'],access_token)

    flag = requests.get(url)

    return flag


def long_lasting_token_2():
    access_token= 'EAAXukhZA5tLEBACXIaGKSlzo8FZBW1sA9PZAuZAXpxzYUJHMu0KddsKvamTG7F3l5gzjZB82UbShnC04d9a90IbTfVAhhIhJOYcmMBVpNxfZATbSZAMNLRsNC9Tv81qJab5AKtkxpKhdONwGrRyOgJ5zofUhajooZC6m0KHCEZCMh1brnRWbiV2fSoZBAo6M7ee8oZD'
    url = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=fb_exchange_token&fb_exchange_token={}'.format(os.environ['APPID_EXPERIMENTS'],os.environ['APPSECRET_EXPERIMENTS'],access_token)

    flag = requests.get(url)

    return flag

def get_page_posts(page_id):
    #access_token
    url = 'https://graphs.facebook.com/oauth/access_token?'


def reading_video_properties(post_id):
    access_token = 'EAAXukhZA5tLEBAHugzUifhrugnWeTrgvtJiInUbFUSyUp1t6AOPc8ZCFUv1o1c0ZBJcnZBzkdOW1MvfcZCPDswXAvEtZAu8mzQ5bT5NbMenImBzwMauDgbcSUjZBWHvK6Hr7zNTU60CfZCZABNzEfeMd5ZCyq14iIE3iBI0ZBPvfnw2ZAgZDZD'
    url = 'https://graph.facebook.com/v2.10/1424450227676325?access_token={}'.format(os.environ['ACCESSTOKEN'])
    flag = requests.get(url)
    return flag

def adding_description(post_id,description):
    #access_token = 'EAAXukhZA5tLEBAHugzUifhrugnWeTrgvtJiInUbFUSyUp1t6AOPc8ZCFUv1o1c0ZBJcnZBzkdOW1MvfcZCPDswXAvEtZAu8mzQ5bT5NbMenImBzwMauDgbcSUjZBWHvK6Hr7zNTU60CfZCZABNzEfeMd5ZCyq14iIE3iBI0ZBPvfnw2ZAgZDZD'
    data = {'description':description}
    url = 'https://graph.facebook.com/v2.10/{}?access_token={}'.format(post_id,access_token)
    flag = requests.post(url,json=data)
    return flag
    #1424450227676325
    