import boto3
import json



sqs = boto3.resource('sqs',region_name = 'eu-west-1')
q = sqs.get_queue_by_name(QueueName='DS_AJM_VIDEO')    


while True:

        messages = []
        #rs = q.get_messages()
        rs = q.receive_messages()
        for m in rs:
            #temp = json.loads(m.get_body())
            temp = json.loads(m.body)
            m.delete()
            try:
                temp = temp['Records'][0]['s3']['object']['key']
                ###AJM commenting out and changing due to difficulty importing 
                #temp = parse.unquote(temp)
                temp = unquote(temp)
                ###
                temp = temp.replace('+',' ')
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            messages.append(temp)

        for message in messages:
            print(message)