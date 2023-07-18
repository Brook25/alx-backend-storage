#!/usr/bin/env python3
""" Redis Module"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    """Redis caching class"""
    def __init__(self):
        """Init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method stores a given value with a key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) ->
            Union[str, int, float, bytes]):
        """Returns a value in the desired format"""
        if fn is not None and callable(fn) and key:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """parametrizes get() with a method that converts to str"""
        return self.get(key, lambda b: b.decode("utf-8"))

    def get_int(seld, key: str) -> int:
        """parametrizes get() with a method that converts to int"""
        return self.get(key, lambda b: int(b))
