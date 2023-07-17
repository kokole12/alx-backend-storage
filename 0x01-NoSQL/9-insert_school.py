#!/usr/bin/env python3
"""python script to insert to mongodb"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """inserting to the database"""
    return mongo_collection.insert(kwargs)
