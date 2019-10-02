import redis
import pandas 


def get_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    out = {}
    for key in r.scan_iter9):
        out.update({key:r.hgetall(key)})
    df = pd.DataFrame(out)
    f = lambda x: x.decode('utf-8')
    df.applymap(f)

    return df