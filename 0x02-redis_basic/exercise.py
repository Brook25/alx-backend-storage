#!/usr/bin/env python3
""" Redis Module"""
import redis
import uuid
from typing import Union


class Cache:
    """Redis caching class"""
    def __init__(self):
        """Init method"""
        self._redis = redis.Redis()
        self._redis.flushall()

    def store(self, data: Union[str, bytes, int, float]) -> None:
        """store a value with a key method"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
