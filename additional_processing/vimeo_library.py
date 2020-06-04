import vimeo
import os 
import time 
import sys

client = vimeo.VimeoClient(
    token = os.environ['VIMEO_ACCESS_TOKEN'],
    key = os.environ['VIMEO_CLIENT_ID'],
    secret = os.environ['VIMEO_CLIENT_SECRET']
)



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

    #return response['link']
    return response


def subtitle_upload(video_uri,file_name,language, track_type = 'subtitles'):
    client.subtitle_upload(video_uri,track_type,language,file_name)
    print('Force')

    


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



    if __name__ == "__main__":
      file_name = sys.argv[1]
      title = sys.argv[2]
      description = sys.argv[3]
      print(file_name)
      print(title)
      print(description)