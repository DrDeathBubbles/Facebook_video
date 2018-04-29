import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process





def fuzzy_matching(talk_title, file_title):
    """
    Fuzzy matching taking the talk title as the input
    And the field_title as the title which is supplied
    """
    return fuzz.ratio(talk_title, file_title)



def get_emails(field_title, data):
    location = data['Full Name'].apply(fuzzy_matching,file_title=field_title)
    location = location.idxmax()
    emails = {}
    emails[field_title] = []
    for i in data.ix[location]['cc'].split(','):
        emails[field_title].append(i.strip())
    return emails 