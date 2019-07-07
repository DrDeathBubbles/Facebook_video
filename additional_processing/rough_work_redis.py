import redis
import pandas as pd 

r = redis.Redis(host='localhost', port = 6379, db=0)


def convert(x):        
    y = {}
    for key, value in x.items():
        key = key.decode("utf-8")
        value = value.decode("utf-8")
        y[key] = value
    return y



keys = r.keys()
temp = []
for key in keys:
    temp.append(convert(r.hgetall(key))