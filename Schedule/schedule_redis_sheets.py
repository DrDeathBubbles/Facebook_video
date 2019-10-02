import redis
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from httplib2 import Http


def get_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    out = {}
    for key in r.scan_iter():
        out.update({key:r.hgetall(key)})
    df = pd.DataFrame(out)
    f = lambda x: x.decode('utf-8')
    df.applymap(f)

    return df

def write_dataframe_to_gsheets(sheet_id, df):
    top_left_cell = 'A1'
    num2alpha = dict(zip(range(1, 27), string.ascii_uppercase))
    bottom_right_cell = num2alpha[len(df.columns)] + str(len(df) + 1)
    cell_ranges = top_left_cell + ':' + bottom_right_cell

    values = df.as_matrix().tolist()
    values.insert(0,list(df.columns))

    write_single_range(sheet_id, cell_ranges, values)

    
def update_schedule(sheet_id, update_frequency):
    schedule_old = pd.DataFrame()
    while True:
        schedule_new = get_redis()
        if schedule_old.equals(schedule_new):
            print('No updates to schedule')
            pass
        else:
            write_dataframe_to_gsheets(sheet_id, schedule_new)
            schedule_old = schedule_new
            print('Schedule updated')

        time.sleep(update_frequency) 

def write_dataframe_to_gsheets(sheet_id, df):
    top_left_cell = 'A1'
    num2alpha = dict(zip(range(1, 27), string.ascii_uppercase))
    bottom_right_cell = num2alpha[len(df.columns)] + str(len(df) + 1)
    cell_ranges = top_left_cell + ':' + bottom_right_cell

    values = df.as_matrix().tolist()
    values.insert(0,list(df.columns))

    write_single_range(sheet_id, cell_ranges, values)

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