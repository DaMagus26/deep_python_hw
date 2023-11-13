import json.decoder
import unittest
from unittest import mock
from parse_json import parse_json


class TestParseJson(unittest.TestCase):
    def test_no_json(self):
        with self.assertRaises(json.decoder.JSONDecodeError):
            parse_json('')

    def test_no_keywords_and_fields(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        parse_json(json_str, keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 0)

    def test_no_keywords(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        parse_json(json_str,
                   required_fields=['key1', 'key2'],
                   keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 0)

    def test_invalid_field(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        parse_json(json_str,
                   required_fields=['key3'],
                   keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 0)

    def test_empty_value(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": ""}'
        parse_json(json_str,
                   required_fields=['key2'],
                   keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 0)

    def test_no_valid_keyword(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        parse_json(json_str,
                   required_fields=['key1', 'key2'],
                   keywords=['word5', 'word6'],
                   keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 0)

    def test_value_word_contains_keyword(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        parse_json(json_str,
                   required_fields=['key2'],
                   keywords=['word'],
                   keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 0)

    def test_single_call(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3"}'
        parse_json(json_str,
                   required_fields=['key2'],
                   keywords=['word3'],
                   keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 1)
        self.assertEqual(mock_callback.call_args, mock.call('key2', 'word3'))

    def test_multiple_valid_fields(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        parse_json(json_str,
                   required_fields=['key1', 'key2'],
                   keywords=['word2', 'word3', 'Word1'],
                   keyword_callback=mock_callback)

        expected_calls = [
            mock.call('key1', 'word2'),
            mock.call('key1', 'Word1'),
            mock.call('key2', 'word3')
        ]

        self.assertEqual(mock_callback.call_count, 3)
        self.assertListEqual(mock_callback.call_args_list, expected_calls)

    def test_ignore_case_for_keyword(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word1 word4"}'
        parse_json(json_str,
                   required_fields=['key1', 'key2'],
                   keywords=['word1'],
                   keyword_callback=mock_callback)

        expected_calls = [
            mock.call('key1', 'Word1'),
            mock.call('key2', 'word1')
        ]

        self.assertListEqual(mock_callback.call_args_list, expected_calls)

    def test_check_case_for_field(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "Key2": "word1 word4"}'
        parse_json(json_str,
                   required_fields=['key1', 'key2'],
                   keywords=['word1'],
                   keyword_callback=mock_callback)

        expected_calls = [
            mock.call('key1', 'Word1'),
        ]

        self.assertListEqual(mock_callback.call_args_list, expected_calls)

    def test_multiple_required_fields_and_keywords(self):
        mock_callback = mock.MagicMock()
        json_str = '{"key1": "word1 word2", "key2": "word1 word4", "key3": "word3 word4"}'
        parse_json(
            json_str,
            required_fields=["key1", "key3"],
            keywords=["word1", "word3", "word4"],
            keyword_callback=mock_callback,
        )

        expected_calls = [
            mock.call("key1", "word1"),
            mock.call("key3", "word3"),
            mock.call("key3", "word4"),
        ]

        self.assertListEqual(mock_callback.call_args_list, expected_calls)

    def test_no_matching_keywords(self):
        mock_callback = mock.MagicMock()
        json_str = '{"key1": "word1 word2", "key2": "word1 word4", "key3": "word3 word4"}'
        parse_json(
            json_str,
            required_fields=["key1", "key3"],
            keywords=["word1", "word3", "word5"],
            keyword_callback=mock_callback,
        )

        expected_calls = [
            mock.call("key1", "word1"),
            mock.call("key3", "word3"),
        ]

        self.assertListEqual(mock_callback.call_args_list, expected_calls)
        
    def test_multiple_keywords_in_one_field(self):
        mock_callback = mock.MagicMock()
        json_str = '{"key1": "word1 word2", "key2": "word2 word2"}'
        parse_json(
            json_str,
            required_fields=["key1", "key2"],
            keywords=["word1", "word2"],
            keyword_callback=mock_callback,
        )
        
        expected_calls = [
            mock.call("key1", "word1"),
            mock.call("key1", "word2"),
            mock.call("key2", "word2"),
            mock.call("key2", "word2"),
        ]
        
        self.assertListEqual(mock_callback.call_args_list, expected_calls)


if __name__ == '__main__':
    unittest.main()
