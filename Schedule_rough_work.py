import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from httplib2 import Http
import pandas as pd
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process


def get_spreadsheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./access_tokens/client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheet_name).sheet1
    # Extract and print all of the values
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
