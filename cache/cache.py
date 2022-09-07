from .lfu import LFUCache


class Cache:

    def __init__(self, shared_cache, capacity=10, ttl=30000):
        self.shared_cache = shared_cache
        self.lfu_cache = LFUCache(capacity, ttl)

    def set(self, key, value):
        self.shared_cache[key] = value
        self.lfu_cache.set(key, value)

    def get(self, key):
        value = self.lfu_cache.get(key)

        if value is None:
            return self.shared_cache.get(key) or -1

        return value
