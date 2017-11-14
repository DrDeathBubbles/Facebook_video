# Talkbot
This is a program for the automated processing and upload of videos to Facebook. It is composed of several files, but most notably
1. Multiprocessing\_master\_control.py 
2. People\_processing.py




## Flow

1. Setup parallel process with 8 workers
2. Establish connection to SQS
3. Acquire the spreadsheets every hour
    * *Speaker talk sheet* which links to _WS\_16\_Speakers_
    * *Speaker email sheet* which links to _Speaker intro Working sheet_
1. Listen to SQS queue 
2. Get message
3. Populate  parallel processing task queue with messages
4. Delete SQS messages 
5. Begin parallel processing section 
3. Move file from S3 to local storage
4. Video process
    * Cut video to start\_time and end\_time
    * Add 3 second fade to the start and end of the video 
    * Save edited video to disk
5. Post processed video to S3 video library bucket
6. Upload video to facebook
    * Check to see if we get a 200 response or 400
    * If 400, wait 6 hours then continue
7. Remove local video file 
8. Get the descripton of the video from spreadsheet and the location of this entry in the spreadsheet
9. Get the speakers of the video
    * Format the speakers into a correct string
10. Format description to include the speakers names
11. Add the description to the facebook video 
12. Get the url of the facebook video
13. Email the speakers the link to the facebook video 
14. Update *speaker talk sheet* with the link to the facebook url


6. Add description
7. Get link
8. Lookup talk in spreadsheet
    1. Update spreadsheet with link to video
    2. Email speakers the link to thgie video
9. Delete local video file
10. Delete mesage from queue.    










# To do




2. Function to Email participants
    1. Using title find speakers
    2. From speaker find email
    3. Email link to speaker


{'Records': [{'eventName': 'ObjectCreated:Put', 'eventVersion': '2.0', 'requestParameters': {'sourceIPAddress': '79.78.94.143'}, 'userIdentity': {'principalId': 'AWS:AIDAJSJVDM427OYOMDUSA'}, 'awsRegion': 'eu-west-1', 's3': {'object': {'versionId': 'GT.re_lQxBodFxFCFVclKgwyrpUsZBlP', 'key': 'Right+metrics+and+wrong+metrics%3A+Is+there+such+a+thing4%3F.mp4', 'eTag': 'b194a0b04d2bc3f99e2b5e19c22a9db3', 'sequencer': '0059F48C8677435203', 'size': 296886272}, 'bucket': {'ownerIdentity': {'principalId': 'A3MRBPFDOQ44CE'}, 'arn': 'arn:aws:s3:::ds.ajm.videos', 'name': 'ds.ajm.videos'}, 's3SchemaVersion': '1.0', 'configurationId': 'DS_AJM_VIDEO_UPLOAD'}, 'eventSource': 'aws:s3', 'eventTime': '2017-10-28T14:48:09.027Z', 'responseElements': {'x-amz-request-id': '0728132753C26972', 'x-amz-id-2': 'lYJBz1Z/gurduD90C21Zj9wHvzPqk0ulzWtA3vCVm1iJ2g5YnqOGSNKeB3DSMyY1q4VvW5lu2oY='}}]}    

Need to add in speakers names to description
Need to add gspread link to video



/home/ubuntu/AJM/video_files/Marketing\ in\ 2018\:\ What\ to\ expect\?.mp4