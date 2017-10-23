import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def get_spreadsheet(spreadsheet):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(spreadsheet).sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    data = pd.DataFrame(list_of_hashes)
    data.columns = data.ix[0]
    return data 

def fuzzy_matching(talk_title, file_title):
     return fuzz.ratio(talk_title, file_title)

def get_speakers(talk_title, field_title,data):
    location = data['Title'].apply(fuzzy_matching,file_title=field_title)
    location = location.idmax()
    speakers = []
    for i in range(1,5):
        speaker = data.ix[location]['Speaker' + str(i)]
        if len(speaker) > 0:
            speaker = speaker.split(',')
            speakers.append(speaker)

    return speakers

if __name__ == '__main__':
    data = get_spreadsheet('WS_16_Speakers')
    location = data['Title'].apply(fuzzy_matching,file_title='How to prevent a cyberwar')
    location = location.idxmax()
    speakers = []
    for i in range(1,5):
        speaker = data.ix[location]['Speaker' + str(i)]
        if len(speaker) > 0:
            speaker = speaker.split(',')
            speakers.append(speaker)
