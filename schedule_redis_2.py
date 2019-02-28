import requests 
import redis
import backoff
import datetime


def formatted_time():
    today = datetime.datetime.now() - datetime.timedelta(minutes=15)
    out = today.strftime('%a, %d %b %Y %H:%M:%S') + " GMT"
    return out 

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
def get_talks(slug):
    """
    This gets the information for all the talks which are in the database
    """
    out = requests.get(f'https://api.cilabs.com/conferences/{slug}/timeslots/',
    headers = {'If-Modified-Since':formatted_time()})
    return out


