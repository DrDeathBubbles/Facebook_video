import pandas as pd 
import os
from shutil import copyfile




def making_files(filename):
    filename = filename.replace('/',' ')

    copyfile('test_trimmed.mp4',filename +'.mp4')



data = pd.read_csv('./WS_16_Speakers.csv', skiprows=1)
data['Title'].dropna().apply(making_files)