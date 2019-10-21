from moviepy.editor import *
#from moviepy.audio.io import AudioFileClip
import moviepy
import time
import timeit





def video_processing(process_name,video_file,sting, watermark, output):
    clip = VideoFileClip(video_file)
    starting_clip = VideoFileClip(sting)
    if clip.size[0] != starting_clip.size[0]:
        print('RESOLUTIONS DO NOT MATCH FOR {}'.format(process_name))
        ratio = starting_clip.size[0]/clip.size[0]
        clip = clip.resize(ratio)

    temp = video_file.split('_')
    start_time = temp[-2]
    end_time = temp[-1].rstrip('.mp4')
    if len(start_time) ==6  and len(end_time) ==6:
        start_time = (int(start_time[0:2]),int(start_time[2:4]),int(start_time[4:6]))
        end_time = (int(end_time[0:2]),int(end_time[2:4]),int(end_time[4:6]))
        clip = clip.subclip(start_time, end_time)
        print('Clip successfully edited')
    else:
        print('Clip not edited ')

    logo = (ImageClip(watermark)
          .set_duration(clip.duration)
          .resize(height=50) 
          .margin(right=8, top=8,bottom =8, left = 8, opacity=0) 
          .set_pos(("right","top")))

    clip = CompositeVideoClip([clip, logo])

    clip = concatenate_videoclips([starting_clip,clip])    
    clip = moviepy.video.fx.all.fadein(clip,6)
    clip = moviepy.video.fx.all.fadeout(clip,6)
    clip.write_videofile(output, temp_audiofile="{}_temp-audio.m4a".format(process_name), 
    remove_temp=False, codec="libx264", audio_codec="aac")



if __name__ == '__main__':
    times = []
    for i in range(0,100):
        start = time.time()
        video_processing('P0','/home/ubuntu/AJM/video_files/b96fd2d5-f2cf-4ad8-83fc-9550eada9ab6_000000_000010.mp4','/home/ubuntu/Talkbot/Facebook_video/sting/RISE_Preroll.mp4','/home/ubuntu/Talkbot/Facebook_video/watermarks/RISE_Logo_Colour.png','./test.mp4')
        end = time.time()
        times.append(end-start)
