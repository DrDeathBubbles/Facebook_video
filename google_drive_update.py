from apiclient import errors
from apiclient.http import MediaFileUpload
from apiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
# ...

def update_file(service, file_id, new_title, new_description, new_mime_type,
                new_filename, new_revision):
  """Update an existing file's metadata and content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to update.
    new_title: New title for the file.
    new_description: New description for the file.
    new_mime_type: New MIME type for the file.
    new_filename: Filename of the new content to upload.
    new_revision: Whether or not to create a new revision for this file.
  Returns:
    Updated file metadata if successful, None otherwise.
  """
  try:
    # First retrieve the file from the API.
    file = service.files().get(fileId=file_id).execute()

    # File's new metadata.
    file['title'] = new_title
    file['description'] = new_description
    file['mimeType'] = new_mime_type

    # File's new content.
    media_body = MediaFileUpload(
        new_filename, mimetype=new_mime_type, resumable=True)

    # Send the request to the API.
    updated_file = service.files().update(
        fileId=file_id,
        body=file,
        #newRevision=new_revision,
        media_body=media_body).execute()
    return updated_file
  except Exception as e: # errors.HttpError, error:
    print('An error occurred: %s' % e)
    #print('An error occurred:')
    return None


if __name__ == '__main__':
    file_id = '1w_PRr6K2kQo-k0LssSMUoVJC9aDVrjCAtBFo5UueW7o'
    store = file.Storage('credentials.json')
    creds = store.get()
    drive_service = build('drive', 'v2', http=creds.authorize(Http()))    
    a = update_file(drive_service, file_id, 'This is the new title', 'This is the new description', 
    'application/octet-stream', './WS_17_stages.csv','True')