from moviepy.editor import *
import moviepy
import sys

def video_processing(video_file,start_time, end_time,output):

    clip = VideoFileClip(video_file)
    #clip = clip.subclip(start_time,end_time)
    clip = moviepy.video.fx.all.fadein(clip,3)
    clip = moviepy.video.fx.all.fadeout(clip,3)
    clip.write_videofile(output)

if __name__ == '__main__':
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    print(sys.argv[4])
    video_processing(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4])
#    video_trimming('/Users/aaronmeagher/Desktop/test_trimmed.mp4')
#    video_processing('/Users/aaronmeagher/Desktop/Trimmed_2.mp4',(10,15),(11,15),'~/Desktop/test_trimmed.mp4')
#video = '/Users/aaronmeagher/Desktop/test_trimmed.mp4'
#clip = VideoFileClip(video).rotate(180)
#clip.write_videofile('/Users/aaronmeagher/Desktop/edited.mp4')