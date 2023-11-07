import unittest
import logging
import fetcher


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.CRITICAL)

    async def test_batch_urls_invalid_path(self):
        with self.assertRaises(OSError):
            await fetcher.batch_fetch('not_existent_path', 1)

    async def test_batch_urls_non_int_num_workers(self):
        with self.assertRaises(TypeError):
            await fetcher.batch_fetch('urls.txt', 1.0)

    async def test_batch_urls_non_invalid_num_workers(self):
        with self.assertRaises(ValueError):
            await fetcher.batch_fetch('urls.txt', 0)


if __name__ == '__main__':
    unittest.main()
