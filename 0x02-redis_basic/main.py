#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

s = cache.store("1st")
print(s)
s1 = cache.store("2nd")
print(s1)
s2 = cache.store("3rd")
print(s2)

inputss = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputss))
print("outputs: {}".format(outputs))
