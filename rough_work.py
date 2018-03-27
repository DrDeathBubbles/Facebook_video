import pandas as pd 
from FB_access_token_generator import get_long_lasting_token_return



def make_json(csv_file):
    data = pd.read_csv(csv_file)
    data.to_json('test.json')


def generate_long_lasting_tokens_dataframe(data):
    if 'long_lasting_token' not in data:
        data['long_lasting_token'] = ''

    token_generator = get_long_lasting_token_return    
    data['long_lasting_token'] = data['access_token'].apply(token_generator)

    return data 


def search_key_2( stages, key):
    out = []
    for i in stages:
        if key == i['id']:
            out.append(i)
#        if key in i.values():
#            out.append(i)
    return out            


class test():
    a = 1

    def test_method(self):
        print(test.a)