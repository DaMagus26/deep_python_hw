import unittest
from unittest import mock
import logging
import json
import fetcher


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.CRITICAL)

    @mock.patch("fetcher.BeautifulSoup")
    def test_most_common_words_short(self, soup_mock):
        soup_mock.get_text = lambda: "mock mock stock poke"
        result = fetcher.most_common_words(soup_mock)
        true_result = {"mock": 2, "stock": 1, "poke": 1}
        self.assertEqual(result, true_result)

    @mock.patch("fetcher.BeautifulSoup")
    def test_most_common_words_long(self, soup_mock):
        soup_mock.get_text = lambda: (
            "mock mock mock stock stock poke poke stroke "
            "stroke talk talk walk walk stalk stalk chalk"
        )
        result = fetcher.most_common_words(soup_mock)
        true_result = {
                "mock": 3,
                "stock": 2,
                "poke": 2,
                "stroke": 2,
                "talk": 2,
                "walk": 2,
                "stalk": 2,
            }
        self.assertEqual(result, true_result)

    def test_parse_page_none(self):
        result = fetcher.parse_page(None)
        self.assertEqual(
            result,
            '{"$error": "Could not connect to page"}'
        )

    def test_parse_page_empty(self):
        result = fetcher.parse_page('')
        self.assertEqual(
            result,
            '{"$error": "Status code is not 200"}'
        )

    def test_parse_page_correct(self):
        result = fetcher.parse_page(
            "mock mock mock stock stock poke poke stroke "
            "stroke talk talk walk walk stalk stalk chalk")
        true_result = {
            "mock": 3,
            "stock": 2,
            "poke": 2,
            "stroke": 2,
            "talk": 2,
            "walk": 2,
            "stalk": 2,
        }
        self.assertEqual(
            result,
            json.dumps(true_result)
        )


if __name__ == '__main__':
    unittest.main()
