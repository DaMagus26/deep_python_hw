import unittest
from unittest import mock
from hw1.text_search import grep
from io import FileIO


class TestGrep(unittest.TestCase):
    def setUp(self) -> None:
        self.file = mock.Mock(spec=FileIO)
        self.file.__enter__ = lambda self: self
        self.file.__exit__ = lambda self, x, y, z: None

    def test_empty_file(self) -> None:
        self.file.readlines.return_value = []
        self.assertListEqual(list(grep(self.file, 'text')), [])

    def test_empty_word(self) -> None:
        self.file.readlines.return_value = ['Some text\n', 'Some other text\n']
        self.assertListEqual(list(grep(self.file, '')), ['Some text\n', 'Some other text\n'])

    def test_no_such_word(self) -> None:
        self.file.readlines.return_value = ['Some text\n', 'Some other text\n']
        self.assertListEqual(list(grep(self.file, 'prison')), [])

    def test_different_cases(self) -> None:
        self.file.readlines.return_value = ['WE HAVE NO MORE TIME LEFT\n']
        self.assertListEqual(list(grep(self.file, 'time')), ['WE HAVE NO MORE TIME LEFT\n'])

    def test_line_start(self) -> None:
        self.file.readlines.return_value = ['Time of our lives\n']
        self.assertListEqual(list(grep(self.file, 'time')), ['Time of our lives\n'])

    def test_line_end(self) -> None:
        self.file.readlines.return_value = ['take your time\n']
        self.assertListEqual(list(grep(self.file, 'time')), ['take your time\n'])

    def test_word_contains_desired_word(self) -> None:
        self.file.readlines.return_value = ['Your timings are off\n']
        self.assertListEqual(list(grep(self.file, 'time')), [])

    def test_multiple_occurrences(self) -> None:
        self.file.readlines.return_value = ['Once upon a time in a town like this\n',
                                            'A little girl made a great big wish\n',
                                            'At the same time miles away\n']
        self.assertListEqual(
            list(grep(self.file, 'time')),
            [
                'Once upon a time in a town like this\n',
                'At the same time miles away\n'
            ])

