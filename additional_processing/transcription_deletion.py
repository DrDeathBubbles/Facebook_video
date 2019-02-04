import boto3


transcribe = boto3.client('transcribe', region_name = 'eu-west-1')
jobs = transcribe.list_transcription_jobs(MaxResults = 100)
jobs = jobs['TranscriptionJobSummaries']
for job in jobs:
    print(job['TranscriptionJobName'])
    transcribe.delete_transcription_job(TranscriptionJobName = job['TranscriptionJobName'])