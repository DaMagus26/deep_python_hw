from typing import Any, Sequence
import re


class FloatListTable:
    def __init__(
            self,
            nrows: int = 0,
            ncols: int = 0,
            fill_value: Any = None) -> None:
        self.data: Sequence[Sequence[float]] = [[fill_value] * ncols] * nrows

    def __get__(self, instance, owner) -> Sequence[Sequence[float]]:
        return self.data

    def __set__(self, instance, value: Sequence[Sequence[float]]):
        if not isinstance(value, list):
            raise TypeError('value must be a list of lists')
        if not all(isinstance(row, list) for row in value):
            raise TypeError('value must be a list of lists')

        lens = [len(row) for row in value]
        if lens:
            if not all(lens[0] == lens[i] for i, _ in enumerate(lens[1:])):
                raise TypeError('all rows must be the same size')

        if not all(isinstance(item, float) for row in value for item in row):
            raise TypeError('all elements must be of type float')

        self.data = value


class Time:
    def __init__(self):
        self.hours: int = 0
        self.minutes: int = 0
        self.seconds: float = 0.0

    def __get__(self, instance, owner) -> float:
        return self.hours * self.minutes + self.seconds / 100

    def __set__(self, instance, value: tuple[int, int, int | float]):
        if not isinstance(value, tuple):
            raise TypeError('value must be a tuple')
        if len(value) != 3:
            raise TypeError(
                'value must have exactly 3 '
                'elements (hours, minutes, seconds)')

        hours, minutes, seconds = value
        if not isinstance(hours, int):
            raise TypeError('hours must be an integer')
        if not isinstance(minutes, int):
            raise TypeError('minutes must be an integer')
        if not isinstance(seconds, (int, float)):
            raise TypeError('seconds must be either integer or float')

        if hours < 0 or hours > 23:
            raise TypeError('hours must be a value between 0 and 23')
        if minutes < 0 or minutes > 59:
            raise TypeError('minutes must be a value between 0 and 59')
        if seconds < 0 or seconds >= 60:
            raise TypeError(
                'seconds must be a value between 0 (inclusive) '
                'and 60 (exclusive)')

        self.hours = hours
        self.minutes = minutes
        self.seconds = float(seconds)


class UserTag:
    def __init__(self) -> None:
        self.tag: str = ''

    def __get__(self, instance, owner) -> str:
        return self.tag

    def __set__(self, instance, value: str):
        if not isinstance(value, str):
            raise TypeError('value must be a string')
        if not value.startswith('@'):
            raise ValueError('tag must always start with @')
        if not 2 < len(value[1:]) < 20:
            raise ValueError(f'tag is too long (max: 20, {len(value)=})')
        pattern = re.compile(r'@[\w_]+')
        if not re.match(pattern, value):
            raise ValueError(
                'tag may only contain digits, english letters and underscore')

        self.tag = value


class DataBase:
    table = FloatListTable()
    last_edited = Time()
    editor_tag = UserTag()


if __name__ == '__main__':
    db = DataBase()
    db.table = {'col1': [1., 2., 3.], 'col2': [4., 5., 6.]}
    print(db.table)
