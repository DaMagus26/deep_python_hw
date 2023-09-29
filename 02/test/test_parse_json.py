import json.decoder
import unittest
from unittest import mock
import sys
sys.path.append('../')
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
        parse_json(json_str, required_fields=['key1', 'key2'], keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 0)

    def test_invalid_field(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        parse_json(json_str, required_fields=['key3'], keyword_callback=mock_callback)

        self.assertEqual(mock_callback.call_count, 0)

    def test_empty_value(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": ""}'
        parse_json(json_str, required_fields=['key2'], keyword_callback=mock_callback)

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
        self.assertEqual(mock_callback.call_args, mock.call('word3'))

    def test_several_valid_fields(self):
        mock_callback = mock.Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        parse_json(json_str,
                   required_fields=['key1', 'key2'],
                   keywords=['word2', 'word3', 'Word1'],
                   keyword_callback=mock_callback)

        expected_calls = [
            mock.call('word2'),
            mock.call('Word1'),
            mock.call('word3'),
        ]

        self.assertEqual(mock_callback.call_count, 3)
        self.assertListEqual(mock_callback.call_args_list, expected_calls)
