import pandas as pd 
import os
from shutil import copyfile




def making_files(filename):
    filename = filename.replace('/',' ')
    copyfile('/Users/aaronmeagher/Desktop/test.mp4','/Users/aaronmeagher/Work/Facebook_test_videos/' +filename +'_000000'+'_000008'+'.mp4')



data = pd.read_csv('./WS_16_Speakers.csv', skiprows=1)
data['Title'].dropna().apply(making_files)