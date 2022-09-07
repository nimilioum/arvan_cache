import time
from unittest import TestCase
from cache import CacheDict


class DictTestCase(TestCase):

    def test_not_timeout(self):
        cache = CacheDict()

        cache['a'] = 1

        self.assertEqual(cache.get('a'), 1)

    def test_timeout(self):
        cache = CacheDict(ttl=5)
        cache['a'] = 1
        time.sleep(0.006)

        self.assertIsNone(cache.get('a'))
