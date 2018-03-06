#This is the section which pulls information from avenger
#Need to put in catch if the talk or the stage is not found!
import requests
import json 
import os 


def avenger_get_talks():
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslots/')
    return out

def avenger_get_talk(id):
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslots/' + str(id))
    return out


def avenger_get_locations():
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslot_locations')
    return out

def avenger_get_locations(timeslot_location_id):
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslot_locations/' + str(timeslot_location_id))
    return out


def avenger_get_attendee_data():
    headers = {'Authorization': 'Bearer {}'.format(os.environ['avenger_token'])}
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/attendances',headers = headers)
    return out