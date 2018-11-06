#This is the section which pulls information from avenger
#Need to put in catch if the talk or the stage is not found!
import requests
import json 
import os 
import datetime 
import re
import string
import backoff 

class avenger_requests():

    def __init__(self, slug):

        self.slug = slug

    def return_unicode_time(self, string):
        """
        This function returns the epoch time in milliseconds. 
        """
        temp_master = re.findall(r"[\w']+", string)
        temp_1 = temp_master[2].split('T')
        temp_master.insert(2,temp_1[0])
        temp_master.insert(3,temp_1[1])
        temp_master.pop(4)
        temp_master[-1] = temp_master[-1].rstrip('Z')
        temp_master = [int(i) for i in temp_master]
        mydate = datetime.datetime(*temp_master[:-1])
        mydate = mydate.timestamp()*1000 + temp_master[-1]
        return mydate


    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get_talks(self):
        """
        This gets the information for all the talks which are in the database
        """
        out = requests.get('https://avenger.cilabs.net/v1/conferences/{}/timeslots/'.format(self.slug))
        return out


    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get_talks_particular(self, id):
        """
        This gets the information about a single talk identified by its UUID
        The 'id' refers to the 'id'. The data is got through .json()['data']['key']
        The id of the talk is returned in the json response object
        lo  
        Returns a response object.
        """
        out = requests.get('https://avenger.cilabs.net/v1/conferences/{}/timeslots/'.format(self.slug) + str(id))
        return out




    #This gets the name of the stage based on the timeslot
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get_locations(self):
        """
        This gets the information of all the stages and their names 
        """
        out = requests.get('https://avenger.cilabs.net/v1/conferences/{}/timeslot_locations'.format(self.slug))
        return out

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get_locations_particular(self, timeslot_location_id):
        """
        This gets the stage information, including name, based on the timeslot_location id
        """
        out = requests.get('https://avenger.cilabs.net/v1/conferences/{}/timeslot_locations/'.format(self.slug) + str(timeslot_location_id))
        return out



    #This is the attendee information section 

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get_attendee_data(self):
        """
        This gets the attendee information for all attendees in Avenger
        """
        headers = {'Authorization': 'Bearer {}'.format(os.environ['avenger_token'])}
        out = requests.get('https://avenger.cilabs.net/v1/conferences/{}/attendances'.format(self.slug),headers = headers)
        return out


    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get_attendee_data_particular(self, attendance_id):
        """
        This gets the attendee information for a particular attendee in Avenger 
        """
        headers = {'Authorization': 'Bearer {}'.format(os.environ['avenger_token'])}
        out = requests.get('https://avenger.cilabs.net/v1/conferences/{}/attendances/{}'.format(self.slug,attendance_id),headers = headers)
        return out
    


    #This section containd the functions which return the data actually needed by TalkBot



    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def speaker_names(self, id):
        """
        Returns the list of speakers for a particular talk

        Takes the talk id and returns a string of the speakers joined by commas with the last
        speaker joined to the string with a 'and'.

        What if there is only one speaker for the talk?
        This does not work - it has to be fixed for the case when there is just one speaker
        """
        talk = self.get_talks_particular(id)
        talk.raise_for_status()
        if 'data' in talk.json().keys():
            speakers = talk.json()['data']['timeslot_participations'] 
            speakers = [self.get_attendee_data_particular(i['attendance_id']).json() for i in speakers]
            speakers = [i['data']['person']['first_name'] + ' ' + i['data']['person']['last_name'] for i in speakers]
            
            printable = set(string.printable)
            f = lambda y : filter(lambda x: x in printable, y)
            speakers = map(f, speakers)            



            return speakers  
        else:
            return








    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def name_processing(self, id):
        """
        Returns the list of speakers for a particular talk

        Takes the talk id and returns a string of the speakers joined by commas with the last
        speaker joined to the string with a 'and'.

        What if there is only one speaker for the talk?
        This does not work - it has to be fixed for the case when there is just one speaker
        """
        talk = self.get_talks_particular(id)
        talk.raise_for_status()
        if 'data' in talk.json().keys():
            speakers = talk.json()['data']['timeslot_participations'] 
            speakers = [self.get_attendee_data_particular(i['attendance_id']).json() for i in speakers]
            speakers = [i['data']['person']['first_name'] + ' ' + i['data']['person']['last_name'] for i in speakers]
            
            
            if len(speakers) == 1:
                speakers = speakers[0]

            elif len(speakers) == 2:
                speakers = ' and '.join(speakers)

            elif len(speakers) > 2:
                speakers = ', '.join(speakers[:-1]) + ' and ' + speakers[-1]

            return speakers  
        else:
            return


    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def title_processing(self, id):
        """
        Given a id of a talk, returns the title of the talk.
        """
        talk = self.get_talks_particular(id)
        talk.raise_for_status()
        if 'data' in talk.json().keys():
            try:
                title = talk.json()['data']['title']
                return title 
            except:
                return None 


    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def description_processing(self, id):
        """
        Given an id of a talk, returns the description of the talk.
        """
        talk = self.get_talks_particular(id)
        talk.raise_for_status()
        if 'data' in talk.json().keys():
            try:
                description = talk.json()['data']['description']
                return description 
            except:
                return None 


    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get_timeslot_id(self, id):
        """
        Given an id of a talk, returns the timeslot of the talk
        """    
        talk = self.get_talks_particular(id)
        talk.raise_for_status()
        if 'data' in talk.json().keys():
            try:
                timeslot_id = talk.json()['data']['timeslot_location_id']
                return timeslot_id
            except:
                return None 


    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get_timeslot_location(self, id):
        """
        Given an id of a talk, returns the string location of that talk
        """
        talk = self.get_talks_particular(id)
        talk.raise_for_status()
        if 'data' in talk.json().keys():
            try:
                timeslot_id = talk.json()['data']['timeslot_location_id']
                return timeslot_id
            except:
                return None 



if __name__ == '__main__':
    test = avenger_requests()
    #a = test.name_processing('2a784db7-f5c7-4418-b895-2de4333efe79')
    a = test.name_processing('70029a23-f8dc-4eb2-89a4-6d7de7409ad9')
    b = test.title_processing('70029a23-f8dc-4eb2-89a4-6d7de7409ad9')
    c = test.description_processing('70029a23-f8dc-4eb2-89a4-6d7de7409ad9')
    #b = a.json()['data']['timeslot_participations']
    #c = [test.get_attendee_data_particular_2(i['attendance_id']).json() for i in b]



