from multiprocessing import managers

from .dict import CacheDict
from .lfu import LFUCache
from .cache import Cache

managers.SharedMemoryManager.register('Dict', CacheDict, managers.DictProxy)
