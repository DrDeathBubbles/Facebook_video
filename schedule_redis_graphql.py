import requests 
import redis
import backoff
import datetime
import pandas as pd 
import time
import arrow 
import avenger_requests_backoff_new_url as avenger_requests
import redis 

def formatted_time():
    today = datetime.datetime.now() - datetime.timedelta(minutes=15)
    out = today.strftime('%a, %d %b %Y %H:%M:%S') + " GMT"
    return out

def convert_time_zone(time):
    time = arrow.get(time)
    time = time.shift(hours = +0)
    return time.format('YYYY/MM/DD HH:mm:ss')   

def get_speakers(x, function):
    f = function(x)
    return f

def clean_speakers(df):
    for row in df['speakers'].iteritems():
        if type(row[1]) == list:
            df['speakers'].iloc[row[0]] = ''
    return df    

def get_participants(participants):
    out = []
    for part in participants['nodes']:
      try:
        if part['attendee']['firstName'] is not None and part['attendee']['lastName'] is not None:
          out.append(part['attendee']['firstName'] + ' ' + part['attendee']['lastName'])
        else:
          out.append(' ')  
      except:
         out.append('') 
    return out

def get_locations(location):
    return location['name']

def speaker_name_processing(speakers):

    if len(speakers) == 1:
        speakers = speakers[0]

    elif len(speakers) == 2:
        speakers = ' and '.join(speakers)

    elif len(speakers) > 2:
        speakers = ', '.join(speakers[:-1]) + ' and ' + speakers[-1]

    else:
        speakers = ''    

    return speakers  




def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.cilabs.com/graphql', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))



def time_schedule_aquisition(talks, slug):
    talks = pd.DataFrame(talks.json()['data'])
    talks = talks[['title','description','start_time','end_time','timeslot_location_id','id']]

    avenger = avenger_requests.avenger_requests(slug)
    locations = avenger.get_locations()
    locations = pd.DataFrame(locations.json()['data'])
    find_location = lambda x: locations[locations['id']== x ]['name'].values[0] 

    talks['timeslot_location_id'] = talks['timeslot_location_id'].apply(find_location)
    talks['start_time'] = talks['start_time'].apply(convert_time_zone)
    talks['end_time'] = talks['end_time'].apply(convert_time_zone)
    talks['speakers'] = talks['id'].apply(get_speakers, function = avenger.name_processing)
    talks['speakers_for_emails'] = talks['id'].apply(get_speakers, function = avenger.speaker_names) 
    talks = clean_speakers(talks)
    
    return talks




def time_schedule_aquisition_2(talks):
    talks = pd.DataFrame(talks['data'])
    temp = []
    for i in talks['conference']['schedule']['days']:
        temp.append(pd.DataFrame(i['timeslots']['nodes']))
    total = pd.concat(temp, ignore_index = True)
    total.fillna('', inplace = True)   
    total['location'] = total['location'].apply(get_locations)
    total['speakers_seed'] = total['participants'].apply(get_participants)
    total['speakers'] = total['speakers_seed'].apply(speaker_name_processing)
    total['speakers_for_emails'] = total['speakers_seed'].apply(','.join)

    total['start_time'] = total['startsAt'].apply(convert_time_zone)
    total['end_time'] = total['endsAt'].apply(convert_time_zone)
    
    out = []
    for i in range(0,len(total)):
      out.append('-'+str(i))
    out = pd.Series(out)  
    
    total['uuid'] = total['location'].str.replace(' ','-').add(out)
    total = total[['title','description','start_time','end_time','location','id','speakers','speakers_for_emails','uuid']]
    return total

def redis_import(row,r):
    #uuid = row['location'].replace(' ','-') + '-' + str(row.name)
    #r_key = row['id'] + ' ' + row['speakers']
    #r_key = uuid + ' ' + row['speakers']
    r_key = row['uuid'] + row['speakers']
    for key in row.keys():
        r.hsetnx(r_key, key, row[key])
    r.hsetnx(r_key,'priority', 0)
    r.hsetnx(r_key,'block',0)    
    r.hsetnx(r_key,'status','Unprocessed')        



def main(query):

    #talks = get_talks_seed(slug)
    talks = run_query(query) 
    r = redis.Redis(host='localhost', port = 6379, db=0)

    while True:

        time_schedule = time_schedule_aquisition_2(talks)
        time_schedule.fillna('',inplace = True)
        time_schedule.apply(redis_import, args=(r,), axis = 1)

#        temp_talks = get_talks_update(slug)
#        if temp_talks.status_code == 304:
#            print('No talks updated')
#        else:
#            print('Updating talks')
#            talks = temp_talks    

        time.sleep(60*15)





if __name__ == '__main__':
   slug = input('Please enter conference slug:')
   query_4 = """
{
  conference(id: "rise19") {
    id
    schedule {
      days {
        timeslots {
          nodes {
            tracks {
              id
            }
            id
            title
            description
            startsAt
            endsAt
            location {
              name
              id
            }
            participants {
              nodes {
                attendee {
                  lastName
                  firstName
                }
              }
            }
          }
        }
      }
    }
  }
}
"""
   main(query_4)
  


