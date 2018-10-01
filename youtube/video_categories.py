# Sample python code for videoCategories.list

import os

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow




CLIENT_SECRETS_FILE = "../credentials/client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def video_categories_list(client, **kwargs):
  # See full sample for function
  #kwargs = remove_empty_kwargs(**kwargs)

  response = client.videoCategories().list(
    **kwargs
  ).execute()

  return response

client = get_authenticated_service()

result = video_categories_list(client,
    part='snippet',
    regionCode='IE')