import requests


test = requests.get('https://api.frame.io/v2/accounts', headers = {"Authorization": f"Bearer {token}"})


url = "https://api.frame.io/v2/accounts/id"


#GET ID
headers_id = {"Accept": "application/json","Authorization": f"Bearer {token}" }
response = requests.request("GET", "https://api.frame.io/v2/accounts/me", headers=headers_id)
##

account_id = 'f7bb64c1-1bd2-4229-b4cd-e70b02c10502'

data = {
  "account_id":f"{account_id}",
  "q": "moon",
  "sort": "name",
  "filter": {
    "inserted_at": [
      {
        "op": "gte",
        "value":"2020-04-01T04:00:00.000Z"
      },
      {
        "op":"lte",
        "value":"2020-04-30T03:59:59.999Z"
      }
    ],
    "project_id": {
      "op": "eq",
      "value":"<project_id>"
      },
    "label": {
      "op": "eq",
       "value": "approved"
    }
  },
  "page_size": 10,
  "page": 1
}

websummit_id = '27c611aa-21bd-4952-905a-7d7749140bb4'
data = {
  "account_id":f"{websummit_id}",
  "q": "WS20_852224863_INT_VOG_V1.mp4",
  "sort": "name",
  "page_size": 10,
  "page": 1
}



search = requests.post('https://api.frame.io/v2/search/library', data = data, headers = headers)


user_accounts = "https://api.frame.io/v2/accounts"
request1 = requests.get(user_accounts, headers = headers)

out = []
for r in request1.json():
    out.append({'display_name': r['display_name','id':r['id']]})

account_id_team = request1.json()[0]['id']


team_accounts = f"https://api.frame.io/v2/accounts/{account_id_team}/teams"
request2 = requests.get(team_accounts, headers = headers)

id = '844745f3-1706-4ffc-a16f-c070ef92b65e'

url = f"https://api.frame.io/v2/assets/{id}"

response = requests.request("GET", url, headers = headers)