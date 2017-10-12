from moviepy.editor import *
import moviepy


def video_processing(video_file,start_time, end_time,output):

    clip = VideoFileClip(video_file)
    clip = clip.subclip(start_time,end_time)
    clip = moviepy.video.fx.all.fadein(clip,3)
    clip.write_videofile(output)

if __name__ == '__main__':
#    video_trimming('/Users/aaronmeagher/Desktop/test_trimmed.mp4')
    video_processing('/Users/aaronmeagher/Desktop/Trimmed_2.mp4',(10,15),(11,15),'~/Desktop/test_trimmed.mp4')
#video = '/Users/aaronmeagher/Desktop/test_trimmed.mp4'
#clip = VideoFileClip(video).rotate(180)
#clip.write_videofile('/Users/aaronmeagher/Desktop/edited.mp4')