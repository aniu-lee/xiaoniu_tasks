#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import hashlib
import time

'''
md5加密
'''
def md5(str=''):
    m = hashlib.md5()
    m.update(str.encode('utf8'))
    return m.hexdigest()

'''
频率限制
'''
def act_limit(uid,action,max_count,period,redis_host='127.0.0.1',redis_port=6379,redis_password=None,redis_db=0):
    import redis
    if redis_password:
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db,password=redis_password)
    else:
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
    r = redis.Redis(connection_pool=pool)
    now = int(time.time())
    expire = int(now / period) * period + period
    ttl = expire - now
    key = "act_limit:%s:%s" % (uid,action)
    count = r.incr(key)
    r.expire(key, ttl)
    if count is False or count > max_count:
        return False
    return True