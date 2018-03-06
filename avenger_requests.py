#This is the section which pulls information from avenger

import requests
import json 

def get_talk():
    a = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslots/')
    return a