import requests 

data = requests.post('https://api.cilabs.com/conferences/cc19/token', json = {'email':'Aaron.Meagher@websummit.com','booking_ref':'SZAP-STF'})

auth_token = data.json()['data']['auth_token']

print(auth_token)