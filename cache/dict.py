import time
from collections import UserDict


def current_milli_time():
    return round(time.time() * 1000)


def get_expire_time(milliseconds, ttl):
    return milliseconds + ttl - (milliseconds % ttl)


class CacheDictValue:

    def __init__(self, value, ttl=30000):
        self.value = value
        self.expire = get_expire_time(current_milli_time(), ttl)

    def __str__(self):
        return f'{self.value}'


class CacheDict(UserDict):

    def __init__(self, ttl=30000):
        self.ttl = ttl
        super().__init__()

    def __setitem__(self, key, value):
        value = CacheDictValue(value, self.ttl)
        super().__setitem__(key, value)

    def __getitem__(self, key):
        try:
            item = self.data[key]

            current = current_milli_time()
            if current >= item.expire:
                raise KeyError

            return item.value

        except KeyError:
            pass
