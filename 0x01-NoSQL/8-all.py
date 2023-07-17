#!/usr/bin/env python3
"""returning all the mongo collections"""
import pymongo


def list_all(mongo_collection):
    if not mongo_collection:
        return []
    documents = mongo_collection.find()
    return [document for document in documents]
