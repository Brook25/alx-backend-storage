#!/usr/bin/env python3
'''Module for counting web requests
'''
import typing, requests
from functools import wraps
import redis


def count_url(fn: typing.Callable) -> typing.Callable:   
    '''decorator counts number of requests
        to a url.
    '''
    r = redis.Redis()
    
    @wraps(fn)
    def wrapper(*args, **kwargs):
        '''modifies get_page'''
        count = r.incr("count:{}".format(*args))
        if int(count) == 1:
            r.expire("count:{}".format(*args), 60)
        print(count)
        return fn(*args, **kwargs)
    return wrapper

@count_url
def get_page(url: str) -> str:
    '''returns html from a requested web page'''
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
