#This is the section which pulls information from avenger
#Need to put in catch if the talk or the stage is not found!
import requests
import json 
import os 
import datetime 



class avenger_requests():

    def return_unicode_time(string):
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



    def get_talks(self):
        """
        This gets the information for all the talks which are in the database
        """
        out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslots/')
        return out

    def get_talks_particular(self, id):
        """
        This gets the information about a single talk identified by its UUID
        The 'id' refers to the 'id'. The data is got through .json()['data']['key']

        Returns a response object.
        """
        out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslots/' + str(id))
        return out




    #This gets the name of the stage based on the timeslot
    def get_locations(self):
        """
        This gets the information of all the stages and their names 
        """
        out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslot_locations')
        return out

    def get_locations_particular(self, timeslot_location_id):
        """
        This gets the stage information, including name, based on the timeslot_location id
        """
        out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/timeslot_locations/' + str(timeslot_location_id))
        return out



    #This is the attendee information section 

    def get_attendee_data(self):
        """
        This gets the attendee information for all attendees in Avenger
        """
        headers = {'Authorization': 'Bearer {}'.format(os.environ['avenger_token'])}
        out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/attendances',headers = headers)
        return out


    def get_attendee_data_particular(self, attendance_id):
        """
        This gets the attendee information for a particular attendee in Avenger 
        """
        headers = {'Authorization': 'Bearer {}'.format(os.environ['avenger_token'])}
        out = requests.get('https://avenger.cilabs.net/v1/conferences/ws17/attendances/{}'.format(attendance_id),headers = headers)
        return out
    

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
            speakers = [test.get_attendee_data_particular(i['attendance_id']).json() for i in speakers]
            speakers = [i['data']['person']['first_name'] + ' ' + i['data']['person']['last_name'] for i in speakers]
            if len(speakers) > 1:
                speakers = ', '.join(speakers) + ' and ' + speakers[-1]
            elif len(speakers) == 1:
                speakers = speakers[0]
            return speakers  
        else:
            return

    def title_processing(self, id):
        talk = self.get_talks_particular(id)
        talk.raise_for_status()
        if 'data' in talk.json().keys():
            try:
                title = talk.json()['data']['title']
                return title 
            except:
                return None 


    def description_processing(self, id):
        talk = self.get_talks_particular(id)
        talk.raise_for_status()
        if 'data' in talk.json().keys():
            try:
                title = talk.json()['data']['description']
                return title 
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



