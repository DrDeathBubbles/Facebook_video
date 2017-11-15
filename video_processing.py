from moviepy.editor import *
import moviepy
import sys

def video_processing(video_file,start_time, end_time,output):

    clip = VideoFileClip(video_file)
    #clip = clip.subclip(start_time,end_time)
    clip = moviepy.video.fx.all.fadein(clip,3)
    clip = moviepy.video.fx.all.fadeout(clip,3)
    clip.write_videofile(output)

def video_processing(video_file, output):
    clip = VideoFileClip(video_file)

    temp = video_file.split('_')
    start_time = temp[4]
    end_time = temp[5].rstrip('.mp4')

    if len(start_time) ==6  and len(end_time) ==6:
        start_time = (start_time[0:2],start_time[2:4],start_time[4:6])
        end_time = (end_time[0:2],end_time[2:4],end_time[4:6])
        clip = clip.subclip(start_time,end_time)

    clip = moviepy.video.fx.all.fadein(clip,3)
    clip = moviepy.video.fx.all.fadeout(clip,3)
    clip.write_videofile(output, remove_temp=True, codex = 'H264', audio_codec = 'aac')



if __name__ == '__main__':
    #print(sys.argv[1])
    #print(sys.argv[2])
    #print(sys.argv[3])
    #print(sys.argv[4])
    #video_processing(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4])
#    video_trimming('/Users/aaronmeagher/Desktop/test_trimmed.mp4')
    video_processing('/home/ubuntu/AJM/video_files/Local_copy.mp4',(10,15),(11,15),'/home/ubuntu/AJM/video_files/Local_copy_3.mp4')
#video = '/Users/aaronmeagher/Desktop/test_trimmed.mp4'
#clip = VideoFileClip(video).rotate(180)
#clip.write_videofile('/Users/aaronmeagher/Desktop/edited.mp4')