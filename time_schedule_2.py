from apiclient import errors
from apiclient.http import MediaFileUpload
from apiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
import avenger_requests
import time
import pandas as pd  
import arrow 
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


def convert_time_zone(time):
    time = arrow.get(time)
    time = time.shift(hours + 0 )
    return time.format('YYYY/MM/DD HH:mm:ss')

if __name__ == '__main__':
    avenger = avenger_requests.avenger_requests()
    talks_old = pd.DataFrame()
    while True:
        talks = avenger.get_talks()
        talks = pd.DataFrame(talks.json()['data'])
        talks = talks[['title','description','start_time','end_time','timeslot_location_id','id']]

        locations = avenger.get_locations()
        locations = pd.DataFrame(locations.json()['data'])
        find_location = lambda x: locations[locations['id']== x ]['name'].values[0] 

        talks['timeslot_location_id'] = talks['timeslot_location_id'].apply(find_location)
        talks['start_time'] = talks['start_time'].apply(convert_time_zone)
        talks['end_time'] = talks['end_time'].apply(convert_time_zone)

        if talks_old.equals(talks):
            print('No updates to talks')
            pass
        else:    

            talks.to_csv('Monc_18_stages.csv')

            #file_id = '1w_PRr6K2kQo-k0LssSMUoVJC9aDVrjCAtBFo5UueW7o'
            file_id = '13b7f2wqgLp2JP5QDbrPiBTgRzHD7wLED_L_m0SUo6QI'
            store = file.Storage('credentials.json')
            creds = store.get()
            drive_service = build('drive', 'v2', http=creds.authorize(Http()))    
            a = update_file(drive_service, file_id, 'Monc_18_stages', 'Monc_18 stage informatiom', 
            'application/octet-stream', './Monc_18_stages.csv','True')
            print('Updated pushed')
            talks_old = talks 
        time.sleep(60*15)