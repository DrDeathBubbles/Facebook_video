import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process



def get_spreadsheets():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    speaker_talk_sheet = client.open('WS_16_Speakers').sheet1
    speaker_email_sheet = client.open('Speaker Intro Working Sheet').sheet1
    # Extract and print all of the values
    hashes_speaker_talk_sheet = speaker_talk_sheet.get_all_records()
    speaker_talk_sheet = pd.DataFrame(hashes_speaker_talk_sheet)
    speaker_talk_sheet.columns = speaker_talk_sheet.ix[0]

    #
    hashes_speaker_email_sheet = speaker_email_sheet.get_all_records()
    speaker_email_sheet = pd.DataFrame(hashes_speaker_email_sheet)
    return [speaker_talk_sheet,speaker_email_sheet]  


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

def update_spreadsheet(location, facebook_url):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open('WS_16_Speakers').sheet1
    sheet.update_acell(location,facebook_url)
    # Extract and print all of the values
    #list_of_hashes = sheet.get_all_records()
    #data = pd.DataFrame(list_of_hashes)
    #data.columns = data.ix[0]
    return sheet 


def fuzzy_matching(talk_title, file_title):
    """
    Fuzzy matching taking the talk title as the input
    And the field_title as the title which is supplied
    """
    return fuzz.ratio(talk_title, file_title)

def get_speakers(field_title,data):
    """
    Getting the speakers for a given talk
    """

    location = data['Title'].apply(fuzzy_matching,file_title=field_title)
    location = location.idxmax()
    speakers = []
    for i in range(1,5):
        speaker = data.ix[location]['Speaker ' + str(i)]
        if len(speaker) > 0:
            speaker = speaker.split(',')
            speakers.append(speaker[0])

    return speakers

def get_emails(speakers,data):
    """
    Gets the email addresses for a given set of speakers
    """
    emails = []
    for speaker in speakers:
        location = data['Full Name'].apply(fuzzy_matching, file_title = speaker)
        location = location.idxmax()
        emails.append(data.ix[location]['email'])
    return emails


def get_description(field_title,data):
    location = data['Title'].apply(fuzzy_matching,file_title=field_title)
    location = location.idxmax()
    talk_title = data.ix[location]['Description']
    if len(talk_title) == 0:
        talk_title = field_title
    return [talk_title,location]


if __name__ == '__main__':
    # Getting spreadsheets
    print('Get spreadsheets')
    speaker_talk_sheet,speaker_email_sheet = get_spreadsheets()

    # Get speakers
    print('Get speakers')
    speakers = get_speakers('Right metrics and wrong metrics: Is there such a thing?',speaker_talk_sheet)
    
    #Get emails
    print('Get emails')
    emails = get_emails(speakers, speaker_email_sheet)
    #Get description
    print('Get description')
    description = get_description('Right metrics and wrong metrics: Is there such a thing?', speaker_talk_sheet)
    