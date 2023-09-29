import unittest
from unittest import mock
import sys
sys.path.append('../')
from timer import mean


class TestTimer(unittest.TestCase):
    def test_zero_repeats(self):
        mock_func = mock.Mock()
        with self.assertRaises(ValueError):
            mean(0)(mock_func)()

    def test_saves_last_return_value(self):
        mock_func = mock.Mock()
        mock_func.return_value = 'Hello, World!'
        result = mean(10)(mock_func)()

        self.assertEqual(result, 'Hello, World!')

    def test_number_of_calls(self):
        mock_func = mock.Mock()
        result = mean(10)(mock_func)()

        self.assertEqual(mock_func.call_count, 10)

    def test_propagates_args(self):
        mock_func = mock.Mock()
        args = ['Hello', 1, ValueError]
        result = mean(10)(mock_func)(*args)

        self.assertEqual(mock_func.call_args, mock.call(*args))