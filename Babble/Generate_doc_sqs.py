from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import boto3
import json
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']



def json_processing(j_obj):
    out = {}
    out['vimeo_url'] = j_obj['Body']['vimeo_url']['StringValue']
    out['s3_url'] = j_obj['Body']['s3_url']['StringValue'] 
    out['uid'] = j_obj['Body']['uid']['StringValue']
    out['speakers'] =  j_obj['Body']['speakers']['StringValue']
    out['text'] =  j_obj['Body']['text']['StringValue']
    out['title'] =  j_obj['Body']['title']['StringValue']
    return out 

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
            creds = flow.run_local_server(port=6677)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    return [drive_service, service]

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'download-from-google-drive-to-s3.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, args)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    
    service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    
    return [drive_service, service]    


def doc_generation( drive_service,service,vimeo_url, s3_url, uid, speakers, text, title):

    document_id = '1szDKqGQYj0w8eze0D5YHr5kJ-XyooagV-moK6-kmK08'
    copy_title = title 
    body = {
        'name': copy_title,
        'parents': ['123a9rNtXvbQeo1etgTXmTAe6G4-XLDPp']
    }
    drive_response = drive_service.files().copy(
    fileId=document_id, body=body).execute()
    document_copy_id = drive_response.get('id')



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
                    'text': '{{vimeo_url}}',
                    'matchCase':  'true'
                },
                'replaceText': vimeo_url,
            }}, 

             {
            'replaceAllText': {
                'containsText': {
                    'text': '{{s3_url}}',
                    'matchCase':  'true'
                },
                'replaceText': s3_url,
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

    sqs = boto3.resource('sqs',region_name = 'eu-west-1')
    q = sqs.get_queue_by_name(QueueName='Babble')    

    while True:
        messages = []
        rs = q.receive_messages()
        for m in rs:
            temp = json.loads(m.body)
            temp = json_processing(temp)
             #To be put back in after testing
            try:
                doc_generation(ser[0], ser[1],**temp)
                m.delete()
                print('Doc generated!')

            except:
                print('Failed to make doc of transcript')
                pass    
















