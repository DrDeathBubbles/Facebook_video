import sys
import os
os.system('command ')
from subprocess import call


if __name__ == '__main__':
#    test = call(['ls','-lrth'])
    test = call(['python3','video_processing.py','/Users/aaronmeagher/Desktop/edited5.mp4','0','10','/Users/aaronmeagher/Desktop/test.mp4'])
