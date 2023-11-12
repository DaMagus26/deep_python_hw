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

        self.assertEqual(cache['k1'], 1)
        self.assertEqual(cache['k2'], 2)
        self.assertEqual(cache['k3'], 3)

    def test_overflow(self):
        cache = LRUCache(2)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3

        self.assertEqual(cache['k1'], None)

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

    def test_size_one(self):
        cache = LRUCache(1)
        cache['k1'] = 10
        self.assertEqual(cache['k1'], 10)

        cache["k2"] = 20
        self.assertEqual(cache['k1'],  None)
        self.assertEqual(cache['k2'],  20)

    def test_overflowing_after_setting_existing_key(self):
        cache = LRUCache(2)
        cache['k1'] = 10
        cache['k2'] = 20
        cache['k1'] = 30
        cache['k3'] = 10

        self.assertEqual(cache['k2'], None)
        self.assertEqual(cache['k3'], 10)
        self.assertEqual(cache['k1'], 30)

    def test_set_existing_key_changes_order(self):
        cache = LRUCache(3)
        cache['k1'] = 10
        cache['k2'] = 20
        cache['k3'] = 30

        cache['k2'] = 40
        cache['k1'] = 50

        # Checking k3
        self.assertEqual(cache['k3'], 30)
        self.assertEqual(cache['k2'], 40)
        self.assertEqual(cache['k1'], 50)
        cache['filler1'] = 0
        self.assertEqual(cache['k3'], None)

        # Checking k2
        self.assertEqual(cache["k2"], 40)
        self.assertEqual(cache["k1"], 50)
        self.assertEqual(cache["filler1"], 0)
        cache["filler2"] = 0
        self.assertEqual(cache["k2"], None)

        # Checking k3
        self.assertEqual(cache["k1"], 50)
        self.assertEqual(cache["filler1"], 0)
        self.assertEqual(cache["filler2"], 0)
        cache["filler3"] = 0
        self.assertEqual(cache["k1"], None)


if __name__ == '__main__':
    unittest.main()
