import pandas as pd 
import os


def making_files(filename):
    print(filename)
    os.system('cp test.mp4 ../video_files/test/{}.mp4'.format(filename))




data = pd.read_csv('./WS_16_Speakers.csv', skiprows=1)
data['Title'].apply(making_files)