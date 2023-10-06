import unittest
import re
from custom_list import CustomList


class CustomArrayAssertsMixin:
    def assertCustomListEqual(
            self,
            lst1: CustomList,
            lst2: CustomList):

        prefix = f'Checking {lst1} and {lst2}\n'
        if not isinstance(lst1, CustomList):
            raise AssertionError(
                prefix +
                f'{lst1} is not an instance of CustomList')
        if not isinstance(lst2, CustomList):
            raise AssertionError(
                prefix +
                f'{lst2} is not an instance of CustomList')
        if len(lst1) != len(lst2):
            raise AssertionError(
                prefix +
                f'Lists have different length: {len(lst1)} and {len(lst2)}')

        for i, (elem1, elem2) in enumerate(zip(lst1, lst2)):
            if elem1 != elem2:
                raise AssertionError(
                    prefix +
                    f'CustomList elements are different at position {i}:'
                    f' {elem1} and {elem2}')


class TestCustomList(unittest.TestCase, CustomArrayAssertsMixin):
    # Testing __init__
    def test_tuple_init(self):
        self.assertCustomListEqual(
            CustomList([1, 2, 3]), CustomList((1, 2, 3)))

    def test_empty_init(self):
        self.assertCustomListEqual(
            CustomList(), CustomList([]))

    def test_set_init(self):
        self.assertCustomListEqual(
            CustomList([1, 2, 3]), CustomList({1, 2, 3}))

    # Testing data types
    def test_invalid_type_add(self):
        with self.assertRaises(TypeError):
            _ = CustomList([1]) + (2)

    def test_invalid_type_sub(self):
        with self.assertRaises(TypeError):
            _ = CustomList([1]) - (2)

    def test_invalid_type_radd(self):
        with self.assertRaises(TypeError):
            _ = (2) + CustomList([1])

    def test_invalid_type_rsub(self):
        with self.assertRaises(TypeError):
            _ = (2) - CustomList([1])

    # Testing __add__
    def test_add_same_length(self):
        self.assertCustomListEqual(
            CustomList([1, 2, 3]) + CustomList([3, 2, 1]),
            CustomList([4, 4, 4])
        )

    def test_add_first_is_shorter(self):
        self.assertCustomListEqual(
            CustomList([1]) + CustomList([3, 2, 1]),
            CustomList([4, 2, 1])
        )

    def test_add_first_is_longer(self):
        self.assertCustomListEqual(
            CustomList([1, 2, 3]) + CustomList([3]),
            CustomList([4, 2, 3])
        )

    def test_add_works_on_lists(self):
        self.assertCustomListEqual(
            CustomList([1, 2, 3]) + [3],
            CustomList([4, 2, 3])
        )

    def test_add_creates_new_object(self):
        x, y = CustomList([1]), CustomList([3])
        new_obj = x + y
        self.assertFalse(new_obj is x)

    # Testing __sub__
    def test_sub_same_length(self):
        self.assertCustomListEqual(
            CustomList([1, 2, 3]) - CustomList([3, 2, 1]),
            CustomList([-2, 0, 2])
        )

    def test_sub_first_is_shorter(self):
        self.assertCustomListEqual(
            CustomList([1]) - CustomList([3, 2, 1]),
            CustomList([-2, -2, -1])
        )

    def test_sub_first_is_longer(self):
        self.assertCustomListEqual(
            CustomList([1, 2, 3]) - CustomList([3]),
            CustomList([-2, 2, 3])
        )

    def test_sub_works_on_lists(self):
        self.assertCustomListEqual(
            CustomList([1, 2, 3]) - [3],
            CustomList([-2, 2, 3])
        )

    def test_sub_creates_new_object(self):
        x, y = CustomList([1]), CustomList([3])
        new_obj = x - y
        self.assertFalse(new_obj is x)

    # Testing __radd__
    def test_radd_same_length(self):
        self.assertCustomListEqual(
            [1, 2, 3] + CustomList([3, 2, 1]),
            CustomList([4, 4, 4])
        )

    def test_radd_first_is_shorter(self):
        self.assertCustomListEqual(
            [1] + CustomList([3, 2, 1]),
            CustomList([4, 2, 1])
        )

    def test_radd_first_is_longer(self):
        self.assertCustomListEqual(
            [1, 2, 3] + CustomList([3]),
            CustomList([4, 2, 3])
        )

    def test_radd_creates_new_object(self):
        x, y = [1], CustomList([3])
        new_obj = x + y
        self.assertFalse(new_obj is x)

    # Testing __sub__
    def test_rsub_same_length(self):
        self.assertCustomListEqual(
            [1, 2, 3] - CustomList([3, 2, 1]),
            CustomList([-2, 0, 2])
        )

    def test_rsub_first_is_shorter(self):
        self.assertCustomListEqual(
            [1] - CustomList([3, 2, 1]),
            CustomList([-2, -2, -1])
        )

    def test_rsub_first_is_longer(self):
        self.assertCustomListEqual(
            [1, 2, 3] - CustomList([3]),
            CustomList([-2, 2, 3])
        )

    def test_rsub_creates_new_object(self):
        x, y = [1], CustomList([3])
        new_obj = x - y
        self.assertFalse(new_obj is x)

    def test_eq(self):
        x, y = CustomList([3, 2, 1]), CustomList([1, 2, 3])
        self.assertEqual(x, y)

    def test_gt(self):
        x, y = CustomList([3, 2, 2]), CustomList([1, 2, 3, 0])
        self.assertGreater(x, y)

    def test_lt(self):
        x, y = CustomList([3, 2, 0]), CustomList([1, 2, 3, 0])
        self.assertLess(x, y)

    def test_ge(self):
        x, y = CustomList([3, 2, 1]), CustomList([1, 2, 3, 0])
        self.assertGreaterEqual(x, y)

    def test_le(self):
        x, y = CustomList([3, 2, 0]), CustomList([1, 2, 3, 0])
        self.assertLessEqual(x, y)

    def test_ne(self):
        x, y = CustomList([3, 2, 2]), CustomList([1, 2, 3, 0])
        self.assertNotEqual(x, y)

    def test_str(self):
        pattern = re.compile(
            r'\[(?:(?:-?\d*\.?\d+)(?:, )?)*\] Sum: (-?\d*\.?\d+)')
        data = [1, 2, 3.2, -1]
        lst = CustomList(data)
        self.assertRegex(str(lst), pattern)
        self.assertEqual(re.match(pattern, str(lst)).group(1), str(sum(data)))


if __name__ == '__main__':
    unittest.main()
