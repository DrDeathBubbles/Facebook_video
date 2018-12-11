import boto3
from moviepy.audio.io import AudioFileClip
import os






if __name__ == '__main__':

    file_location = '/home/ubuntu/AJM/video_files/'


    s3 = boto3.resource('s3')

    my_bucket = s3.Bucket('ws18-videos')
    my_bucket_destination = s3.Bucket('ws18-audio')
    get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))

    unsorted = []

    for file in my_bucket.objects.filter():
        unsorted.append(file)


    files = [obj.key for obj in sorted(unsorted, key=get_last_modified, reverse=True)][1:]

    i = 1.0
    total = len(files) 

    for file in files:
        i = i + 1
        my_bucket.download_file(file, file_location + file )
        try:
            temp = AudioFileClip.AudioFileClip(file_location + file)
        except:
            print('Oops, cannot process this audio file')
            with open('Failures.txt','a') as f:
                f.write(file)
            continue     
        audio_file =  file.rstrip('.mp4') + '.mp3' 
        temp.write_audiofile(file_location + 'audio/' + audio_file) 
        my_bucket_destination.upload_file(file_location + 'audio/' + audio_file, '{}'.format(audio_file))
        os.remove(file_location + file)
        print(i/total)
        print(file)

