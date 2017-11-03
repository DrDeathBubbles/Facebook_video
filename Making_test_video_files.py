import pandas as pd 
import os
import unicodedata

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))




def making_files(filename):
    print(filename)
    filename = slugify(filename)
    print(filename)
    os.system('cp test.mp4 /home/ubuntu/AJM/video_files/test/{}.mp4'.format(filename))




data = pd.read_csv('./WS_16_Speakers.csv', skiprows=1)
data['Title'].dropna().apply(making_files)