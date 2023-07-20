#!/usr/bin/env python3
"""Module for Redis caching class"""
import redis
import uuid
from typing import Union, Optional, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''decorator func with a wrapper to count number of call on cache.store
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''wrapper fn that does the counting and store the result in redisdb
        '''
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''decorator that stores arguments passed to method'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''wrapper stores arguments passed'''
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    '''function prints out the history of a Cache method'''
    if method:
        _redis = getattr(method.__self__, '_redis', None)
        if _redis:
            key = method.__qualname__
            inputs = _redis.lrange(key + ":inputs", 0, -1)
            outputs = _redis.lrange(key + ":outputs", 0, -1)
            count = 0 if not _redis.get(key) else int(_redis.get(key))
            print('{} was called {} times:'.format(key, count))
            for _in, out in zip(inputs, outputs):
                print("{}(*{}) -> {}".format(key, _in.decode('utf-8'),
                                             out.decode('utf-8')))


class Cache:
    """Redis caching class"""
    def __init__(self):
        """Init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method stores a given value with a key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) ->\
            Union[str, int, float, bytes]:
        """Returns a value in the desired format"""
        if fn is not None and callable(fn) and key:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """parametrizes get() with a method that converts to str"""
        return self.get(key, lambda b: b.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """parametrizes get() with a method that converts to int"""
        return self.get(key, lambda b: int(b))
