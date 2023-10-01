import unittest
from unittest import mock
from io import FileIO
from text_search import grep


class TestGrep(unittest.TestCase):
    def setUp(self) -> None:
        self.file = mock.Mock(spec=FileIO)
        self.file.__enter__ = lambda self: self
        self.file.__exit__ = lambda self, x, y, z: None

    def test_empty_file(self) -> None:
        self.file.__iter__ = lambda s: iter([])
        self.assertListEqual(list(grep(self.file, ['text'])), [])

    def test_empty_word(self) -> None:
        self.file.__iter__ = lambda s: iter(['Some text\n', 'Some other text\n'])
        self.assertListEqual(
            list(grep(self.file, [''])), ['Some text\n', 'Some other text\n'])

    def test_no_such_word(self) -> None:
        self.file.__iter__ = lambda s: iter(['Some text\n', 'Some other text\n'])
        self.assertListEqual(list(grep(self.file, ['prison'])), [])

    def test_different_cases(self) -> None:
        self.file.__iter__ = lambda s: iter(['WE HAVE NO MORE TIME LEFT\n'])
        self.assertListEqual(
            list(grep(self.file, ['time'])), ['WE HAVE NO MORE TIME LEFT\n'])

    def test_line_start(self) -> None:
        self.file.__iter__ = lambda s: iter(['Time of our lives\n'])
        self.assertListEqual(
            list(grep(self.file, ['time'])), ['Time of our lives\n'])

    def test_line_end(self) -> None:
        self.file.__iter__ = lambda s: iter(['take your time\n'])
        self.assertListEqual(
            list(grep(self.file, ['time'])), ['take your time\n'])

    def test_word_contains_desired_word(self) -> None:
        self.file.__iter__ = lambda s: iter(['Your timings are off\n'])
        self.assertListEqual(list(grep(self.file, ['time'])), [])

    def test_multiple_occurrences(self) -> None:
        self.file.__iter__ = lambda s: iter([
            'Once upon a time in a town like this\n',
            'A little girl made a great big wish\n',
            'At the same time miles away\n'
        ])
        self.assertListEqual(
            list(grep(self.file, ['time'])),
            [
                'Once upon a time in a town like this\n',
                'At the same time miles away\n'
            ])

    def test_multiple_words(self) -> None:
        self.file.__iter__ = lambda s: iter([
            'Once upon a time in a town like this\n',
            'A little girl made a great big wish\n',
            'At the same time miles away\n',
            'A little boy made a wish that say\n'
        ])
        self.assertListEqual(
            list(grep(self.file, ['time', 'big'])),
            [
                'Once upon a time in a town like this\n',
                'A little girl made a great big wish\n',
                'At the same time miles away\n'
            ])

    def test_more_than_one_word_in_a_line(self) -> None:
        self.file.__iter__ = lambda s: iter([
            'Once upon a time in a town like this\n',
            'A little girl made a great big wish\n',
            'At the same time miles away\n',
            'A little boy made a wish that say\n'
        ])
        self.assertListEqual(
            list(grep(self.file, ['time', 'town'])),
            [
                'Once upon a time in a town like this\n',
                'At the same time miles away\n'
            ])


if __name__ == '__main__':
    unittest.main()
