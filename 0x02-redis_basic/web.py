#!/usr/bin/env python3
"""Web caching in redis"""
from functools import wraps
import requests
import redis

db = redis.Redis()


def count_url_requests(method):
    """decorator to count calls"""
    @wraps(method)
    def wrapper(url):
        cache_key = "cached: {}".formate(url)
        catched_data = db.get(cache_key)
        if catched_data:
            return catched_data.decode('urf-8')
        count_key = "count:" + url
        html = method(url)

        db.incr(count_key)
        db.set(cache_key, html)
        db.expire(cache_key, 10)
        return html
    return wrapper


@count_url_requests
def get_page(url: str) -> str:
    """returns html"""
    res = requests.get(url)
    return res.text
