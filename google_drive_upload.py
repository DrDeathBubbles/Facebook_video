from googleapiclient.http import MediaFileUpload
from apiclient.discovery import build


#drive_service = build('drive', 'v2', http=http)
drive_service = build('drive', 'v3', http=creds.authorize(Http()))
file_metadata = {
    'name': 'My Report',
    'mimeType': 'application/vnd.google-apps.spreadsheet'
}
media = MediaFileUpload('WS_17_stages.csv',
                        mimetype='text/csv',
                        resumable=True)
file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
print('File ID: %s' % file.get('id'))