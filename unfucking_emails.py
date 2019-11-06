import redis

r = redis.Redis(host='localhost', port = 6379, db=0,decode_responses=True)

out = {}

for key in r.scan_iter():
    out.update({key:r.hgetall(key)})

f = lambda x: x.day


date = pd.to_datetime(df['start_time']).apply(f)

first_day = df[date == 5.0]


for row in first_day.iterrows():
    if (row[1]['IGNORE_Emails_resent'] == '1') and (row[1]['resend_emails'] == '1') and (row[1]['speakers'] != 'Barbara Martin Coppola, Kristin Lemkau and Cheng Lei'):
        print(row)
        r.hset(row[0],'IGNORE_Emails_resent', 0)