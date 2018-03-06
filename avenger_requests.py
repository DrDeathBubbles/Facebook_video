#This is the section which pulls information from avenger
#Need to put in catch if the talk or the stage is not found!
import requests
import json 
import os 



def avenger_get_talks():
    """
    This gets the information for all the talks which are in the database
    """
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslots/')
    return out

def avenger_get_talk(id):
    """
    This gets the information about a single talk identified by its UUID
    """
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslots/' + str(id))
    return out




#This gets the name of the stage based on the timeslot
def avenger_get_locations():
    """
    This gets the information of all the stages and their names 
    """
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslot_locations')
    return out

def avenger_get_locations(timeslot_location_id):
    """
    This gets the stage information, including name, based on the timeslot_location id
    """
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslot_locations/' + str(timeslot_location_id))
    return out



#This is the attendee information section 

def avenger_get_attendee_data():
    """
    This gets the attendee information for all attendees in Avenger
    """
    headers = {'Authorization': 'Bearer {}'.format(os.environ['avenger_token'])}
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/attendances',headers = headers)
    return out


def avenger_get_attendee_data(attendance_id):
    """
    This gets the attendee information for a particular attendee in Avenger 
    """
    headers = {'Authorization': 'Bearer {}'.format(os.environ['avenger_token'])}
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/attendances/{}'.format(attendance_id),headers = headers)
    return out