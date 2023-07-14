#!/usr/bin/env python3
"""creating a cache class"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """counting the number of calls to a method"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wraps the method as adecorator"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorated function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(fn: Callable):
    '''display the history of calls of a particular function.'''
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
