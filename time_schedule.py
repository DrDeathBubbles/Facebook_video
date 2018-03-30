import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import avenger_requests


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


def get_stage_name(timeslot_location_id,locations):
    temp = locations[locations['id']==timeslot_location_id]['name']
    return temp.values[0]


if __name__ == '__main__':
    sheet = get_spreadsheet('CC_18_timesheet')
    avenger = avenger_requests.avenger_requests()
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