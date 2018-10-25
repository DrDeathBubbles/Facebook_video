import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from httplib2 import Http
import pandas as pd
import avenger_requests
import arrow
import string
import time
from fuzzywuzzy import fuzz 



def find_row(df, field_title, search_term):
    fuzzy_matching = lambda a,b : fuzz.ratio(a,b)
    location = df[field_title].apply(fuzzy_matching,b=search_term)
    location = location.idxmax()
    return location


def get_spreadsheet(sheet_name):
    """
    Returns a dataframe containing all the values in the first sheet of a gsheet

    sheet_name (str): The string name of the sheet - not the id of the sheet!

    """

    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./access_tokens/client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    sheet = sheet.get_all_records()
    sheet = pd.DataFrame(sheet)
    return sheet 

def read_single_range(spreadsheet_id, range_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./access_tokens/client_secret.json', scope)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    result = service.spreadsheets().values().get( spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result


def write_single_range(spreadsheet_id,range_name,values,value_input_option='RAW'):
    """
    Writes a range of values to a spreadsheet

    spreadsheet_id (str): the id of the spreadsheet obtained from the url of the spreadsheet
    range_name (str): the ranges to be written in the spreadsheet of the form "A1:B12". Single cell - "A1:A1"
    values (array): the values to be unpacked, given in a nested array [[1,2,3],[4,5,6]]. Single cell - [['Test']]
    value_input_option: default - RAW - insert and read as plain text and do not excute as formulas

    """
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./access_tokens/client_secret.json', scope)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    body ={'values':values}
    result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption=value_input_option, body=body).execute()


def convert_time_zone(time):
    time = arrow.get(time)
    time = time.shift(hours = +0)
    return time.format('YYYY/MM/DD HH:mm:ss')    

def get_speakers(x, function):
    f = function(x)
    time.sleep(1)
    return f


def time_schedule_aquisition(slug):
    avenger = avenger_requests.avenger_requests(slug)
    talks = avenger.get_talks()
    talks = pd.DataFrame(talks.json()['data'])
    talks = talks[['title','description','start_time','end_time','timeslot_location_id','id']]

    locations = avenger.get_locations()
    locations = pd.DataFrame(locations.json()['data'])
    find_location = lambda x: locations[locations['id']== x ]['name'].values[0] 

    talks['timeslot_location_id'] = talks['timeslot_location_id'].apply(find_location)
    talks['start_time'] = talks['start_time'].apply(convert_time_zone)
    talks['end_time'] = talks['end_time'].apply(convert_time_zone)
    talks['speakers'] = talks['id'].apply(get_speakers, function = avenger.name_processing)
    return talks

def write_dataframe_to_gsheets(sheet_id, df):
    top_left_cell = 'A1'
    num2alpha = dict(zip(range(1, 27), string.ascii_uppercase))
    bottom_right_cell = num2alpha[len(df.columns)] + str(len(df) + 1)
    cell_ranges = top_left_cell + ':' + bottom_right_cell

    values = df.as_matrix().tolist()
    values.insert(0,list(df.columns))

    write_single_range(sheet_id, cell_ranges, values)


def update_schedule(sheet_id, slug, update_frequency):
    schedule_old = pd.DataFrame()
    while True:
        schedule_new = time_schedule_aquisition(slug)
        if schedule_old.equals(schedule_new):
            print('No updates to schedule')
            pass
        else:
            write_dataframe_to_gsheets(sheet_id, schedule_new)
            schedule_old = schedule_new
            print('Schedule updated')

        time.sleep(update_frequency)                        

if __name__ == '__main__':
    #a = read_single_range('1LafAM4Ru3fZYEyt44J-Pixul0VV4Yfxmvu7hr5te-vg','A1:D4')        
    #b = write_single_range('1LafAM4Ru3fZYEyt44J-Pixul0VV4Yfxmvu7hr5te-vg','A1:D4',[['This','Is','A','Test'],[1,2,3,4]])
    #Below is for ws18
    sheet_id = '1LafAM4Ru3fZYEyt44J-Pixul0VV4Yfxmvu7hr5te-vg'
    update_schedule(sheet_id,'ws18',60*60)