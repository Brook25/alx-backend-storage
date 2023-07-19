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
    def wrapper(self, *args, **kwargs) -> Any:
        '''wrapper stores arguments passed'''
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, args[0])
        self._redis.rpush(method.__qualname__ + ":outputs", str(output))
        return output
    return wrapper


class Cache:
    """Redis caching class"""
    def __init__(self):
        """Init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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



cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))
