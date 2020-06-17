from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']



def service_generation():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    return [drive_service, service]


def doc_generation(drive_service,service):

    document_id = '1szDKqGQYj0w8eze0D5YHr5kJ-XyooagV-moK6-kmK08'
    copy_title = 'Copy Title'
    body = {
        'name': copy_title
    }
    drive_response = drive_service.files().copy(
    fileId=document_id, body=body).execute()
    document_copy_id = drive_response.get('id')




    title = 'Alice'
    text = 'This is the text of the talk'
    speakers = 'Aaron J Meagher'
    vimeo_link = 'vimeo.com'

    requests = [
         {
            'replaceAllText': {
                'containsText': {
                    'text': '{{title}}',
                    'matchCase':  'true'
                },
                'replaceText': title,
            }},

            {
            'replaceAllText': {
                'containsText': {
                    'text': '{{speakers}}',
                    'matchCase':  'true'
                },
                'replaceText': speakers,
            }}, 

             {
            'replaceAllText': {
                'containsText': {
                    'text': '{{vimeo_link}}',
                    'matchCase':  'true'
                },
                'replaceText': vimeo_link,
            }}, 

             {
            'replaceAllText': {
                'containsText': {
                    'text': '{{title}}',
                    'matchCase':  'true'
                },
                'replaceText': title,
            }}, 

             {
            'replaceAllText': {
                'containsText': {
                    'text': '{{text}}',
                    'matchCase':  'true'
                },
                'replaceText': text,
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=document_copy_id, body={'requests': requests}).execute()

    return result        



if __name__ == '__main__':
    ser =service_generation()
    temp = doc_generation(*ser) 
















