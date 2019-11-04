import pandas as pd 
import redis
import uuid

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




def row_processing(row):
    output = {}
    id_ = str(uuid.uuid5(uuid.NAMESPACE_DNS, row['Talk']))
    print(id_)

    output['title'] = row['Talk']
    output['Speaker'] = row['Speaker']
    output['Stage'] = row['Stage']
    output['priority'] = 0
    output['block'] = 0
    output['set_private'] = 0
    output['resend_emails'] = 0
    output['upload_to_youtube'] = 0
    output['vimeo_link'] = ''
    output['youtube_link'] = ''
    output['s3_link_public'] = ''
    output['s3_link_raw'] = ''
    output['status'] = 'Unprocessed'
    output['IGNORE_Emails_resent'] = 0
    output['id'] = id_ 
    output['uuid'] = id_
    output['speakers_for_emails'] = row['Speaker']
    output['speakers'] = speaker_name_processing(row['Speaker'].split(','))



    r.hmset(id_,output)









r = redis.Redis(host='localhost', port = 6379, db=0)

xls = pd.ExcelFile('../WS_19_stages.xlsx')

stages_2 = pd.read_excel(xls, 'Stage 2')
stages_3 = pd.read_excel(xls, 'Stage 3')
stage_51 = pd.read_excel(xls, 'Stage 5, Day 1')
stage_52 = pd.read_excel(xls, 'Stage 5, Day 2')
stage_53 = pd.read_excel(xls, 'Stage 5, Day 3')
stage_81 = pd.read_excel(xls, 'Stage 8, Day 1')
stage_823 = pd.read_excel(xls, 'Stage 8, Day 2&3')



stages_2.apply(row_processing, axis = 1)



