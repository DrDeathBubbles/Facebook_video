
# Talkbot


# Deployment

1. Start processing system
    python3 CFH_main.py 

1. Open tunnel between processing system and scheduling system
    1. 










# Talkbot
This is a program for the automated processing and upload of videos to Facebook. It is composed of several files, but most notably Multiprocessing\_master\_control.py, People\_processing.py and Email\_processing.py



## Setup

Install the python requirements using pip3 install -r requirements.txt in the virtualenv. 


1. Install the python requirements using pip3 install -r requirements.txt
2. Setup the SQS monitoring of the bucket. This is a two step process.
    1. Create new queue - standard queue. Note, only one type of queue is useable by the bucket feed.
    1. In the the bucket go to properties/
    2. Go into events.
    3. Add notifications and add Put Post, send to SQS queue and select the created queue from above.
3.  











## Getting facebook page access tokens
The page access tokens are acquired from the manage_pages function from the FB_access_token_generator module. Run this with the access token 
associated with the account to get a list of all pages managed by this token and their access tokens.

This is needed for generating the facebook page access tokens

https://stackoverflow.com/questions/20180836/the-access-token-does-not-belong-to-application-trying-to-generate-long-lived

We need stage_id -> (page_id,access_token)

Need to be a page admin to have page appear on the manage_pages method 


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



## File naming convention

The files are named as follows:

_uuid\_StartTime\_EndTime.mp4_

The leading string does not matter in the processing, as long as there is an *_* before the uuid of the talk
and the StartTime and EndTime are the second last and last strings respectively.

The StartTime and EndTime are measured from the start of the video file. The StartTime and EndTime are in the format HHMMSS where H - hours, M - minutes and S - seconds. For example, if the end time of the video is after 1 hour, 23 minutes and 12 seconds, and the beginning time was at 0 hours, 1 minute and 9 seconds, the resulting string for the uploaded video would be:

_uuid\_000109\_012312.mp4_


## To do

1. Return json objects from avenger_requests.py 
2. check to see if response is correct and throw error if not
2. Change main.py to use json objects instead of checking for responses
3. Change main.py so that variables are placed in the function for :
    * Change video processing so that watermark is functionalised
    * Change video processing so that sting is functionalised 
    * Change main so that buckets are setup correctly 
4. Change main.py so that variables are all defined in the __main__ and not set in the functions themselves


7. Add control to add playlists
8. Add section which determines the number of cpus available and uses all but two

10. Update readme with deployment and use of the code 
11. Make proper exclusion list which reads from google sheet and processes these every cycle 
12. Fix people processing
13. Schedule
    * Make each stage appear in its own tab
    * Make exclusion column with 1 or 0 in it 
    * Update column with not uploaded, uploaded, processing, processed, published, link
    * Put section to update talk description  

14. Setup proper monitoring for talkbot showing ongoing processes
15. Setup sheet which states which videos have been processed, link to video, and success or failure - google sheet
16. Tests :P
17. Set flag for local or server operation    
18. Retrry queue
19. Delete objects from the queue
20. Put variables as default for video processing - not hard coded
21. Clean up html_python_file 
22. Change how avenger_requests is called 
23. Start main with conference slug
24. Setup WS18 bucket 
25. Make s3 bucket for ws18
26. Change sqs message from facebook to youtube
27. Fix loggin
28. Open bucket for public download
29. Functionalise transcription
30. Add sqs for transcription jobs
31. Investigate updating youtube metadata with keywords
32.  

## Done
5. Strip out facebook functions which are no longer necessary
6. Introduce youtube upload function
9. Make a main function for main.py 

## Notes about main.py

* It looks like _path\_to\_videos_ and _file\_location_ do the same thing. These need to be fixed 

## Resourse which are of interest to this project
This is the logging information 

https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes

https://github.com/jruere/multiprocessing-logging




### Notes
uuid = 'f0bd7b1d-d8b3-4a3c-803f-d32f56e08638'


#NLTK
https://www.analyticsvidhya.com/blog/2018/02/the-different-methods-deal-text-data-predictive-python/


## Email flow

The flow of the emails is as follows:

1. In *main.py*, the _process\_message_ function calls _send\_email_
2. _send\_email_ is imported from *Email_processing.py*. It has several functions:
    1. 
    1. It imports from *./email\_html/html\_python\_file.py* the function _html\_email\_processing\_3_
3. 



## SQS ERROR

Traceback (most recent call last):
  File "./logging/queuehandler.py", line 60, in emit
    self.enqueue(self.prepare(record))
  File "./logging/queuehandler.py", line 27, in enqueue
    self.queue.put_nowait(record)
AttributeError: 'sqs.Queue' object has no attribute 'put_nowait'
Logged from file connectionpool.py, line 396
Traceback (most recent call last):
  File "./logging/queuehandler.py", line 60, in emit
    self.enqueue(self.prepare(record))
  File "./logging/queuehandler.py", line 27, in enqueue
    self.queue.put_nowait(record)
AttributeError: 'sqs.Queue' object has no attribute 'put_nowait'
Logged from file _common.py, line 77


##SQS messsage from upload

{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"eu-west-1","eventTime":"2019-02-05T15:01:25.803Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AIDAJSJVDM427OYOMDUSA"},"requestParameters":{"sourceIPAddress":"89.101.27.89"},"responseElements":{"x-amz-request-id":"71BAF6E333676EA0","x-amz-id-2":"fe/GVq3Othx5aHk7UkewTHeMFGO+dlGMcQvOQAOLUFUyh8y8WWRfj9ZqpHNVDtf+ULV0VgygQxU="},"s3":{"s3SchemaVersion":"1.0","configurationId":"DS_AJM_VIDEO_UPLOAD","bucket":{"name":"ds-ajm-videos","ownerIdentity":{"principalId":"A3MRBPFDOQ44CE"},"arn":"arn:aws:s3:::ds-ajm-videos"},"object":{"key":"test.mp4","size":11340176,"eTag":"ca69605b2d5e5ade854af8381beff3d2","versionId":"Y1h8ir9D3i_fpDEgFAjPqFTHB6BRWTEj","sequencer":"005C59A544A94BC581"}}}]}



## s4cmd 