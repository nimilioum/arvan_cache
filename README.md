### Design
All the cache implementation is inside cache package.

cache.Cache is the 2 level cache

Inside LFU cache I incremented capacity by 1, because if we 
have capacity of 100, the 100th node will be the last key that was used
by set method instead of 100th most frequently used key, 
so by making the capacity 101, the cache will work correctly.

### TODO
* add a decorator, so we can cache every function just by the decorator
* add more tests