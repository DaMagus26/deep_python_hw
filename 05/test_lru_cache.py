import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_zero_size(self):
        with self.assertRaises(ValueError):
            _ = LRUCache(0)

    def test_non_integer_size(self):
        with self.assertRaises(TypeError):
            _ = LRUCache(1.3)

    def test_correct_storing(self):
        cache = LRUCache(3)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3

        self.assertEqual(
            cache.state, {'k1': 1, 'k2': 2, 'k3': 3}
        )

    def test_overflow(self):
        cache = LRUCache(2)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3

        self.assertEqual(
            cache.state, {'k2': 2, 'k3': 3}
        )

    def test_reordering(self):
        cache = LRUCache(3)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3
        _ = cache['k2']

        self.assertEqual(
            cache.state, {'k1': 1, 'k3': 3, 'k2': 2}
        )

    def test_access_invalid_key(self):
        cache = LRUCache(3)
        result = cache['k1']
        self.assertIs(result, None)

    def test_access_deleted(self):
        cache = LRUCache(2)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3
        result = cache['k1']
        self.assertIs(result, None)

    def test_example(self):
        cache = LRUCache(2)

        cache["k1"] = "val1"
        cache["k2"] = "val2"

        self.assertIs(cache["k3"], None)
        self.assertEqual(cache["k2"], "val2")
        self.assertEqual(cache["k1"], "val1")

        cache["k3"] = "val3"

        self.assertEqual(cache["k3"], "val3")
        self.assertIs(cache["k2"], None)
        self.assertEqual(cache["k1"], "val1")


if __name__ == '__main__':
    unittest.main()
