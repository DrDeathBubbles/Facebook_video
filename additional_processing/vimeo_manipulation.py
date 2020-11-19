import vimeo
import os 
import time 
import sys

client = vimeo.VimeoClient(
    token = os.environ['VIMEO_ACCESS_TOKEN'],
    key = os.environ['VIMEO_CLIENT_ID'],
    secret = os.environ['VIMEO_CLIENT_SECRET']
)


def 


def set_privacy_status(video_id, privacy = 'disable'):
  uri = f'https://api.vimeo.com/videos/{video_id}'
  test = client.patch(uri, data = {'privacy':{'view':privacy,'embed': 'whitelist'}})
  return test

def set_whitelist_domain(video_id, domain = 'live.collisionconf.com'):
  out = client.put(f'https://api.vimeo.com/videos/{video_id}/privacy/domains/{domain}')
  return out 



def vimeo_upload(file_name, title, description,privacy='anybody'):

    
    uri = client.upload(file_name, data={
        'name':f'{title}',
        'description':f'{description}',
        'privacy':{'view':f'{privacy}'}
    })

    while True: 
        response = client.get(uri + '?fields=transcode.status').json()
        if response['transcode']['status'] == 'complete':
          print('Your video finished transcoding.')
          break
        elif response['transcode']['status'] == 'in_progress':
          print('Your video is still transcoding.')
        else:
          print('Your video encountered an error during transcoding.')
          return -1 
        time.sleep(60) 


    response = client.get(uri + '?fields=link').json()

    return response['link']


def subtitle_upload(video_uri,file_name,language = 'en-US', track_type = 'subtitles'):
    video_uri = '/videos/' + video_uri.split('/')[3]
    out = client.upload_texttrack(video_uri,track_type,language,file_name)
    return out


    if __name__ == "__main__":
      file_name = sys.argv[1]
      title = sys.argv[2]
      description = sys.argv[3]
      print(file_name)
      print(title)
      print(description)