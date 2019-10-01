import requests 
import redis
import backoff
import datetime
import pandas as pd 
import time
import arrow 
import avenger_requests_backoff_new_url as avenger_requests
import redis 

def formatted_time():
    today = datetime.datetime.now() - datetime.timedelta(minutes=15)
    out = today.strftime('%a, %d %b %Y %H:%M:%S') + " GMT"
    return out

def convert_time_zone(time):
    time = arrow.get(time)
    time = time.shift(hours = +0)
    return time.format('YYYY/MM/DD HH:mm:ss')   

def get_speakers(x, function):
    f = function(x)
    return f

def clean_speakers(df):
    for row in df['speakers'].iteritems():
        if type(row[1]) == list:
            df['speakers'].iloc[row[0]] = ''
    return df    


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
def get_talks_seed(slug):
    """
    This gets the information for all the talks which are in the database
    """
    out = requests.get(f'https://api.cilabs.com/conferences/{slug}/timeslots/')
    return out


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
def get_talks_update(slug):
    """
    This gets the information for all the talks which are in the database
    Returns 304 if no changes have been made in the last 15 minutes
    Returs 200 if changes have been made 
    """
    out = requests.get(f'https://api.cilabs.com/conferences/{slug}/timeslots/',
    headers = {'If-Modified-Since':formatted_time()})
    return out


def time_schedule_aquisition(talks, slug):
    talks = pd.DataFrame(talks.json()['data'])
    talks = talks[['title','description','start_time','end_time','timeslot_location_id','id']]

    avenger = avenger_requests.avenger_requests(slug)
    locations = avenger.get_locations()
    locations = pd.DataFrame(locations.json()['data'])
    find_location = lambda x: locations[locations['id']== x ]['name'].values[0] 

    talks['timeslot_location_id'] = talks['timeslot_location_id'].apply(find_location)
    talks['start_time'] = talks['start_time'].apply(convert_time_zone)
    talks['end_time'] = talks['end_time'].apply(convert_time_zone)
    talks['speakers'] = talks['id'].apply(get_speakers, function = avenger.name_processing)
    talks = clean_speakers(talks)
    
    return talks


def redis_import(row,r):
    r_key = row['id'] + ' ' + row['speakers']
    for key in row.keys():
        r.hsetnx(r_key, key, row[key])
    r.hsetnx(r_key,'priority', 0)
    r.hsetnx(r_key,'block',0)    
    r.hsetnx(r_key,'status','Unprocessed')        



def main(slug):

    talks = get_talks_seed(slug)
    r = redis.Redis(host='localhost', port = 6379, db=0)

    while True:

        time_schedule = time_schedule_aquisition(talks,slug)        
        time_schedule.apply(redis_import, args=(r,), axis = 1)

        temp_talks = get_talks_update(slug)
        if temp_talks.status_code == 304:
            print('No talks updated')
        else:
            print('Updating talks')
            talks = temp_talks    

        time.sleep(60*15)





if __name__ == '__main__':
   presets = input('Please enter conference slug:') 
   main(presets)
  


