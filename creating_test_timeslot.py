import redis


r = redis.Redis(host='localhost', port = 6379, db=0)


test_slot = {'title':'DS TEST TITLE', 'description':'DS TEST DESCRIPTION', 'start_time':'2019/05/21 13:45:00', 'end_time':'2019/05/21 14:00:00',
'timeslot_location_id':'Centre Stage','id':'b96fd2d5-f2cf-4ad8-83fc-9550eada9ab6','uuid':'b96fd2d5-f2cf-4ad8-83fc-9550eada9ab6', 'speakers': 'Aaron Meagher', 'priority':'0', 'block': '0',
'resend_emails':0,'set_private':0,'vimeo_link':'','youtube_link':'','s3_link_public':'','s3_link_raw':'','IGNORE_Emails_resent':0,
'status': 'Unprocessed','speakers_for_emails': 'Aaron Meagher'}


r.hmset('b96fd2d5-f2cf-4ad8-83fc-9550eada9ab6 Aaron Meagher', test_slot)