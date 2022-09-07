from unittest import TestCase
from multiprocessing import Pool, Process, managers
from cache import Cache


def task1(shared_cache):
    cache = Cache(shared_cache)

    cache.set(1, 1)
    cache.set(2, 2)

    return cache


def task2(shared_cache):
    cache = Cache(shared_cache)

    cache.set(3, 3)
    cache.set(4, 4)

    return cache


class CacheTestCase(TestCase):

    def setUp(self) -> None:
        self.smm = managers.SharedMemoryManager()
        self.smm.start()

    def tearDown(self) -> None:
        self.smm.shutdown()

    def test_process_cache(self):

        shared_cache = self.smm.Dict()

        with Pool(processes=2) as pool:
            r1 = pool.apply_async(task1, (shared_cache,))
            r2 = pool.apply_async(task2, (shared_cache,))

            res1 = r1.get(10)
            res2 = r2.get(10)

            self.assertEqual(len(res1.lfu_cache.cache), 2)
            self.assertEqual(len(res2.lfu_cache.cache), 2)
            self.assertEqual(len(shared_cache), 4)
