import redis


r = redis.Redis(host='localhost', port = 6379, db=0)


test_slot = {'title':'DS TEST TITLE', 'description':'DS TEST DESCRIPTION', 'start_time':'2019/05/21 13:45:00', 'end_time':'2019/05/21 14:00:00',
'timeslot_location_id':'Centre Stage','id':'6a069e0c-ea96-4516-b047-ef919173test', 'speakers': 'Aaron Meagher', 'priority':'0', 'block': '0',
'status': 'Unprocessed'}


r.hmset('6a069e0c-ea96-4516-b047-ef919173test Aaron Meagher', test_slot)