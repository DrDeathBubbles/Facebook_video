# Talkbot
This is a program for the automated processing and upload of videos to Facebook. It is composed of several files, but most notably Multiprocessing\_master\_control.py, People\_processing.py and Email\_processing.py



# Setup

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


#To do new
1. Upgrade api to new version of api
2. Develop access token checkers which self heal the auth tokens
3. Generate access keys json file



#Resourse which are of interest to this project
This is the logging information 

https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes





