#This is the section which pulls information from avenger

import requests
import json 

def avenger_get_talk():
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslots/')
    return out


def avenger_get_locations():
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslot_locations')
    return out

def avenger_get_attendee_data():
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI3MDU5ZGUzNC01NjZmLTQyNWMtYWQ5YS01ZTAyN2VkZDhjYWEiLCJqdGkiOiIwN2QzYjgyMy1iN2Y3LTQ2NjctYTRmMi04OTcxZmMyNGM1MjIiLCJpYXQiOjE1MDkzODA0NDUsImFkbWluIjpmYWxzZSwiYXR0X2lkIjoiMTE5NjVjMzItMDJjYy00Y2Y1LWExOTYtY2IyYzIxZDk3YzY5In0.jdMksOC8UI2zj5IgIw0NoT9iDsprT0UofYheD9vSxaE'}
    out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/attendances',headers = headers)
    return out