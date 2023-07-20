#!/usr/bin/env python3
'''Module for counting web requests
'''
import typing
import requests
from functools import wraps
import redis


r = redis.Redis()


def count_url(fn: typing.Callable) -> typing.Callable:
    '''decorator counts number of requests
        to a url.
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        '''modifies get_page'''
        r.incr("count:{}".format(*args))
        res = fn(*args)
        if not r.get("res:{}".format(*args)):
            r.setex("res:{}".format(*args), 10, res)
        return res
    return wrapper


@count_url
def get_page(url: str) -> str:
    '''returns html from a requested web page'''
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
