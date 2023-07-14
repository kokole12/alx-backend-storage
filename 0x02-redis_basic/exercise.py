#!/usr/bin/env python3
"""creating a cache class"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: callable) -> Callable:
    """counting the number of calls to a method"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wraps the method as adecorator"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid4)
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """converting data back to format"""
        val = self._redis.get(key)
        if fn:
            value = fn(val)
        return val

    def get_str(self, key: str) -> str:
        """parametizec Cache.get()"""
        val = self._redis.get(key).decode('utf-8')
        return val

    def get_int(self, key: str) -> int:
        """parametizing Cache.get() to format"""
        val = self._redis.get(key)
        try:
            val = int(val.decode('utf-8'))
        except Exception:
            val = 0
        return val