# Flow

1. Listen to queue
2. Get message
3. Move file from S3 to local storage
4. Video process
5. Upload video to facebook
6. Add description
7. Get link
8. Lookup talk in spreadsheet
    1. Update spreadsheet with link to video
    2. Email speakers the link to the video
9. Delete local video file
10. Delete mesage from queue.    



# To do
1. Delete local copy of files
2. Add speakers name to descriptiomn
3. Add to gspread the link to the video

2. FIX URL

3. UPDATE SPREADSHEET WITH URL

2. Function to Email participants
    1. Using title find speakers
    2. From speaker find email
    3. Email link to speaker


{'Records': [{'eventName': 'ObjectCreated:Put', 'eventVersion': '2.0', 'requestParameters': {'sourceIPAddress': '79.78.94.143'}, 'userIdentity': {'principalId': 'AWS:AIDAJSJVDM427OYOMDUSA'}, 'awsRegion': 'eu-west-1', 's3': {'object': {'versionId': 'GT.re_lQxBodFxFCFVclKgwyrpUsZBlP', 'key': 'Right+metrics+and+wrong+metrics%3A+Is+there+such+a+thing4%3F.mp4', 'eTag': 'b194a0b04d2bc3f99e2b5e19c22a9db3', 'sequencer': '0059F48C8677435203', 'size': 296886272}, 'bucket': {'ownerIdentity': {'principalId': 'A3MRBPFDOQ44CE'}, 'arn': 'arn:aws:s3:::ds.ajm.videos', 'name': 'ds.ajm.videos'}, 's3SchemaVersion': '1.0', 'configurationId': 'DS_AJM_VIDEO_UPLOAD'}, 'eventSource': 'aws:s3', 'eventTime': '2017-10-28T14:48:09.027Z', 'responseElements': {'x-amz-request-id': '0728132753C26972', 'x-amz-id-2': 'lYJBz1Z/gurduD90C21Zj9wHvzPqk0ulzWtA3vCVm1iJ2g5YnqOGSNKeB3DSMyY1q4VvW5lu2oY='}}]}    

Need to add in speakers names to description
Need to add gspread link to video



/home/ubuntu/AJM/video_files/Marketing\ in\ 2018\:\ What\ to\ expect\?.mp4