import redis
from Email_processing import *
from People_processing_CC import *
import time 
import pandas as pd

r = redis.Redis(host='localhost', port = 6378, db=0,decode_responses=True)
 

def main(speaker_email_data):
    out = {}
    for key in r.scan_iter():
        out.update({key:r.hgetall(key)})
    df = pd.DataFrame(out)
    df = df.transpose()
    df.fillna('',inplace = True)

    df = df[(df['resend_emails']=='1') & (df['IGNORE_Emails_resent'] =='0')]
    for row in df.iterrows():
        key = row[0]
        data = row[1]
        youtube_url = data['youtube_link']
        vimeo_url = data['vimeo_link']
        s3_link_public = data['s3_link_public']
        speakers_for_emails = data['speakers_for_emails'].split(',')

        print(speakers_for_emails)
        for speaker in speakers_for_emails:
            emails = get_emails_cc(str(speaker), speaker_email_data)
            print(emails)
            send_email_all_links(emails[0],emails[1],youtube_url, vimeo_url, s3_link_public)

    r.hset(key,'IGNORE_Emails_resent','1')     




if __name__ == '__main__':
    speaker_email_data = pd.read_csv('./stages_speakers/WS19_emails.csv')
    speaker_email_data.fillna('',inplace=True)
    while True:
        main(speaker_email_data)
        time.sleep(60*5)