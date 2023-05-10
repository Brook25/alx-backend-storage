#!/usr/bin/env python3
"""
module implements an expiring web cache and tracker
"""
from typing import Callable
from functools import wraps
import redis
import requests
redis_client = redis.Redis()


def url_count(method: Callable) -> Callable:
    """counts how many times the url is accessed"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_client.incr(f"count:{url}")
        cachd = redis_client.get(f'{url}')
        if cachd:
            return cachd.decode('utf-8')
        redis_client.setex(f'{url}, 10, {method(url)}')
        return method(*args, **kwargs)
    return wrapper


@url_count
def get_page(url: str) -> str:
    """get a page and cache value"""
    res = requests.get(url)
    return res.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
