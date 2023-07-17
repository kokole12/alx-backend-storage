#!/usr/bin/env python3
"""prototype: def list_all(mongo_collection):"""
import pymongo


def list_all(mongo_collection):
    """returning all the documentations"""
    if not mongo_collection:
        return []
    documents = mongo_collection.find()
    return [document for document in documents]
