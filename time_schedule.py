import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import avenger_requests
import time 
import tenacity

def get_spreadsheet(spreadsheet):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(spreadsheet).sheet1

    # Extract and print all of the valus
    #list_of_hashes = sheet.get_all_records()
    #data = pd.DataFrame(list_of_hashes)
    #data.columns = data.ix[0]
    return sheet


@tenacity.retry(wait=tenacity.wait_exponential())
def insert_row(sheet, temp, i):
    try:
        sheet.insert_row(temp[i],i+2)
        print(i)
    except:
        print('there has been an interruption')


if __name__ == '__main__':
    sheet = get_spreadsheet('CC_18_timesheet')
    avenger = avenger_requests.avenger_requests()
    while True:
        talks = avenger.get_talks()
        talks = pd.DataFrame(talks.json()['data'])
        talks = talks[['title','description','start_time','end_time','timeslot_location_id','id']]

        locations = avenger.get_locations()
        locations = pd.DataFrame(locations.json()['data'])
        find_location = lambda x: locations[locations['id']== x ]['name'].values[0] 

        talks['timeslot_location_id'] = talks['timeslot_location_id'].apply(find_location)

        temp = []
        for row in talks.iterrows():
            index,data = row
            temp.append(data.tolist())

        for i in range(0,len(temp)):
            insert_row(sheet,temp,i)            


#    sheet = get_spreadsheet('CC_18_timesheet')
#    avenger = avenger_requests.avenger_requests()
#    columns = ['title','description','start_time','end_time','timeslot_location_id','id'] 
#    index = pd.RangeIndex(0,220)
#    old_talks = pd.DataFrame(index = index, columns = columns)


#    while True:
#
#        new_talks = avenger.get_talks()
#        new_talks = pd.DataFrame(new_talks.json()['data'])
#        new_talks = talks[['title','description','start_time','end_time','timeslot_location_id','id']]
#        ne_stacked = (old_talks != new_talks).stack() 
#
#
#
#
#
#        time.sleep(60*60)
#


#https://stackoverflow.com/questions/45182819/getting-error-when-accessing-a-sheet-in-google-drive-through-api




