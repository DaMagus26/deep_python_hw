import unittest
from unittest import mock
from timer import AvgExecTime


class TestTimer(unittest.TestCase):
    def test_zero_repeats(self):
        mock_func = mock.Mock()
        with self.assertRaises(ValueError):
            AvgExecTime(0)(mock_func)()

    def test_saves_last_return_value(self):
        mock_func = mock.Mock()
        mock_func.return_value = 'Hello, World!'
        result = AvgExecTime(10)(mock_func)()

        self.assertEqual(result, 'Hello, World!')

    def test_number_of_calls(self):
        mock_func = mock.Mock()
        AvgExecTime(10)(mock_func)()

        self.assertEqual(mock_func.call_count, 1)

    def test_propagates_args(self):
        mock_func = mock.Mock()
        args = ['Hello', 1, ValueError]
        AvgExecTime(10)(mock_func)(*args)

        self.assertEqual(mock_func.call_args, mock.call(*args))


if __name__ == '__main__':
    unittest.main()
