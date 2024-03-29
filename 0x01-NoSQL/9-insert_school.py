#!/usr/bin/env python3
""" Python function that inserts a
    new document into a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Returns the new _id
    """
    id = mongo_collection.insert(kwargs)
    return id
