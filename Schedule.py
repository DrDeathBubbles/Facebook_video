import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from httplib2 import Http
import pandas as pd
import avenger_requests
import arrow
import string
import time 


def get_spreadsheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./access_tokens/client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    sheet = sheet.get_all_records()
    sheet = pd.DataFrame(sheet)
    sheet.columns = sheet.iloc[0]
    return sheet 

def read_single_range(spreadsheet_id, range_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./access_tokens/client_secret.json', scope)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    result = service.spreadsheets().values().get( spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result


def write_single_range(spreadsheet_id,range_name,values,value_input_option='RAW'):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./access_tokens/client_secret.json', scope)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    body ={'values':values}
    result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption=value_input_option, body=body).execute()


def convert_time_zone(time):
    time = arrow.get(time)
    time = time.shift(hours = +8)
    return time.format('YYYY/MM/DD HH:mm:ss')    


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
    a = read_single_range('1LafAM4Ru3fZYEyt44J-Pixul0VV4Yfxmvu7hr5te-vg','A1:D4')        
    b = write_single_range('1LafAM4Ru3fZYEyt44J-Pixul0VV4Yfxmvu7hr5te-vg','A1:D4',[['This','Is','A','Test'],[1,2,3,4]])