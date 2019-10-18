import redis
from Email_processing import *
from People_processing_CC import *
import time 
import pandas as pd

r = redis.Redis(host='localhost', port = 6379, db=0,decode_responses=True) 

def main():
    out = {}
    for key in r.scan_iter():
        out.update({key:r.hgetall(key)})
    df = pd.DataFrame(out)
    df = df.transpose()


    return df





if __name__ == '__main__':
    while True:
        main()
        time.sleep(60*5)