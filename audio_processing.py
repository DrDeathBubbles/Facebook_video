import boto3
from moviepy.audio.io import AudioFileClip
import os






if __name__ == '__main__':

    file_location = '/home/ubuntu/AJM/video_files/'


    s3 = boto3.resource('s3')

    my_bucket = s3.Bucket('cc18-videos')

    get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))

    unsorted = []

    for file in my_bucket.objects.filter():
        unsorted.append(file)


    files = [obj.key for obj in sorted(unsorted, key=get_last_modified, reverse=True)][0:250]

    i = 0.0
    total = len(files) 

    for file in files:
        print(file)
        my_bucket.download_file(file, file_location + file )
        temp = AudioFileClip.AudioFileClip(file_location + file)
        audio_file =  file.rstrip('.mp4') + '.mp3' 
        temp.write_audiofile(file_location + 'audio/' + audio_file) 
        my_bucket.upload_file(file_location + 'audio/' + audio_file, 'CC18_audio/{}'.format(audio_file))
        os.remove(file_location + file)
        print(i/total)

