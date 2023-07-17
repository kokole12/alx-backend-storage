#!/usr/bin/env python3
"""updating values using pymongo"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """udating the values in  documents"""
    return mongo_collection.update_many({"name": name},
                                        {"$set": {"topics": topics}})
