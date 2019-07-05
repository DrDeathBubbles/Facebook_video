import requests
import os
import base64

test = requests.get('https://api.vimeo.com/me/videos', headers = ('Authorization': os.environ['VIMEO_ACCESS_TOKEN'] ))


test = requests.get('https://api.vimeo.com/me/videos', headers = ('Authorization': (os.environ['VIMEO_CLIENT_ID'],os.environ['VIMEO_CLIENT_SECRET']))



test = requests.get('https://api.vimeo.com/me/videos', headers = {'Authorization': (base64.b64encode(os.environ['VIMEO_CLIENT_ID'].encode('utf-8')),base64.b64encode(os.environ['VIMEO_CLIENT_SECRET'].encode('utf-8')))})