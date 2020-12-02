import os
from frameioclient import FrameioClient

token = 'fio-u-mTMmGXevbXIDnTsFlGmC2MQgTvISaSQfLZPrQzI_nKwwB0tfEfZfTJkHDQ3Nzf-C' 

client = FrameioClient(token)
me = client.get_me()
print(me['id'])


account_id = me['account_id']

teams = client.get_teams(account_id)

for item in team_ids:
  print('Team ID: {}'.format(team['id']))