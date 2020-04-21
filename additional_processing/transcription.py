from __future__ import print_function
import time
import boto3
transcribe = boto3.client('transcribe')
#job_name = "job name"
job_name = 'AJM_TEST_WS18'
#job_uri = "https://S3 endpoint/test-transcribe/answer2.wav"
job_uri = "https://s3-eu-west-1.amazonaws.com/cc18-videos/CC18_audio/09713108-36c7-4232-bde7-2a2ece553088_The_sole_obligation_of_a_firm_is_to_create_wealth_for_its_shareholders.mp3"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='en-US'
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
print(status)