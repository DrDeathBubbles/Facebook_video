import redis
import pandas as pd 

r = redis.Redis(host='localhost', port = 6379, db=0)


keys = r.keys()
temp = []
for key in keys:
    temp.append(r.hgetall(key))