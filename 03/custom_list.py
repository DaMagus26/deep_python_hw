from typing import Sequence


class CustomList(list):
    def __init__(self, lst: Sequence | None = None):
        lst = lst or []
        super().__init__(lst)

    def __add__(self, other):
        if not isinstance(other, list):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' + {self.__class__} and {type(other)}')

        new_list = []
        for i in range(max(len(self), len(other))):
            if i >= len(self):
                new_list.extend(other[i:])
                break
            if i >= len(other):
                new_list.extend(self[i:])
                break

            new_list.append(self[i] + other[i])

        return self.__class__(new_list)

    def __sub__(self, other):
        if not isinstance(other, list):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' - {self.__class__} and {type(other)}')

        new_list = []
        for i in range(max(len(self), len(other))):
            if i >= len(self):
                new_list.extend([x * -1 for x in other[i:]])
                break
            if i >= len(other):
                new_list.extend(self[i:])
                break

            new_list.append(self[i] - other[i])

        return self.__class__(new_list)

    def __radd__(self, other):
        if not isinstance(other, list):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' + {type(other)} and {self.__class__}')

        new_list = []
        for i in range(max(len(self), len(other))):
            if i >= len(self):
                new_list.extend(other[i:])
                break
            if i >= len(other):
                new_list.extend(self[i:])
                break

            new_list.append(self[i] + other[i])

        return self.__class__(new_list)

    def __rsub__(self, other):
        if not isinstance(other, list):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' - {type(other)} and {self.__class__}')

        new_list = []
        for i in range(max(len(self), len(other))):
            if i >= len(self):
                new_list.extend(other[i:])
                break
            if i >= len(other):
                new_list.extend([x * -1 for x in self[i:]])
                break

            new_list.append(other[i] - self[i])

        return self.__class__(new_list)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' == {self.__class__} and {type(other)}')

        return sum(self) == sum(other)

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' <= {self.__class__} and {type(other)}')

        return sum(self) <= sum(other)

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' >= {self.__class__} and {type(other)}')

        return sum(self) >= sum(other)

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' != {self.__class__} and {type(other)}')

        return sum(self) != sum(other)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' < {self.__class__} and {type(other)}')

        return sum(self) < sum(other)

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f'unsupported operand type(s) for'
                f' > {self.__class__} and {type(other)}')

        return sum(self) > sum(other)

    def __str__(self):
        return super().__str__() + f' Sum: {sum(self)}'


if __name__ == '__main__':
    # Проверить списки, кортежи и множества в качестве входных значений
    print([1, 2, 3, 4, 5] - (CustomList([3, 2, 1, 0])))
