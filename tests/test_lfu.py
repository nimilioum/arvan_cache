from unittest import TestCase
from cache import LFUCache


class LFUTestCase(TestCase):

    def test_cache(self):
        lfu = LFUCache(capacity=2)

        lfu.set(1, 1)
        lfu.set(2, 2)
        lfu.set(3, 3)
        lfu.set(4, 4)

        self.assertEqual(lfu.get(1), -1)
        self.assertEqual(lfu.get(2), 2)
        self.assertEqual(lfu.get(3), 3)
        self.assertEqual(lfu.get(4), 4)

    def test_cache_2(self):
        lfu = LFUCache(capacity=2)

        lfu.set(1, 1)
        lfu.set(2, 2)
        lfu.set(5, 5)
        lfu.set(3, 3)
        lfu.set(4, 4)
        lfu.set(3, 3)
        lfu.set(4, 4)

        self.assertEqual(lfu.get(3), 3)
        self.assertEqual(lfu.get(4), 4)
        self.assertEqual(lfu.get(1), -1)
        self.assertEqual(lfu.get(2), -1)
