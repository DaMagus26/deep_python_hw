import unittest
from descriptors import Time, UserTag, FloatListTable


class TestFloatListTable(unittest.TestCase):
    def test_type(self):
        class DataBase:
            table = FloatListTable()

        self.assertIsInstance(DataBase.table, list)

    def test_not_list(self):
        class DataBase:
            table = FloatListTable()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.table = {'col1': [], 'col2': []}

    def test_inconsistent_row_types(self):
        class DataBase:
            table = FloatListTable()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.table = [[1, 2], 1]

    def test_inconsistent_sizes(self):
        class DataBase:
            table = FloatListTable()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.table = [[1, 2], [1, 2, 3]]

    def test_float(self):
        class DataBase:
            table = FloatListTable()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.table = [[1., 2.], [1., 2]]

    def test_empty(self):
        class DataBase:
            table = FloatListTable()

        db = DataBase()
        db.table = []
        self.assertEqual(db.table, [])

    def test_alright(self):
        class DataBase:
            table = FloatListTable()

        db = DataBase()
        db.table = [[1., 2.], [1., 2.]]
        self.assertEqual(db.table, [[1., 2.], [1., 2.]])


class TestTime(unittest.TestCase):
    def test_type(self):
        class DataBase:
            edit_time = Time()

        self.assertIsInstance(DataBase.edit_time, float)

    def test_tuple(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.edit_time = [1, 2, 3]

    def test_invalid_length(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.edit_time = (1, 2, 3, 4)

    def test_invalid_hour_type(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.edit_time = (1.5, 2, 3)

    def test_invalid_hour_range(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.edit_time = (-1, 2, 3)

        with self.assertRaises(TypeError):
            db.edit_time = (24, 2, 3)

    def test_invalid_minute_type(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.edit_time = (1, 2.2, 3)

    def test_invalid_minute_range(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.edit_time = (1, -1, 3)

        with self.assertRaises(TypeError):
            db.edit_time = (1, 60, 3)

    def test_invalid_second_type(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.edit_time = (1, 2, 3+2j)

    def test_invalid_second_range(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.edit_time = (1, 2, -1)

        with self.assertRaises(TypeError):
            db.edit_time = (1, 2, 60)

    def test_all_correct(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        db.edit_time = (14, 42, 31.015)
        self.assertEqual(db.edit_time, 588.31015)

    def test_result_type(self):
        class DataBase:
            edit_time = Time()

        db = DataBase()
        db.edit_time = (14, 42, 30)
        self.assertIsInstance(db.edit_time, float)


class TestUserTag(unittest.TestCase):
    def test_type(self):
        class DataBase:
            editor_tag = UserTag()

        self.assertIsInstance(DataBase.editor_tag, str)

    def test_not_str(self):
        class DataBase:
            editor_tag = UserTag()

        db = DataBase()
        with self.assertRaises(TypeError):
            db.editor_tag = 123

    def test_at(self):
        class DataBase:
            editor_tag = UserTag()

        db = DataBase()
        with self.assertRaises(ValueError):
            db.editor_tag = 'killer_dominator228'

    def test_invalid_length(self):
        class DataBase:
            editor_tag = UserTag()

        db = DataBase()
        with self.assertRaises(ValueError):
            db.editor_tag = '@_XxX_killer_dominator228_XxX_'

    def test_invalid_symbols(self):
        class DataBase:
            editor_tag = UserTag()

        db = DataBase()
        with self.assertRaises(ValueError):
            db.editor_tag = '@--invalid_tag$$'

    def test_empty(self):
        class DataBase:
            editor_tag = UserTag()

        db = DataBase()
        with self.assertRaises(ValueError):
            db.editor_tag = '@'

    def test_all_correct(self):
        class DataBase:
            editor_tag = UserTag()

        db = DataBase()
        db.editor_tag = '@damagus'
        self.assertEqual(db.editor_tag, '@damagus')


if __name__ == '__main__':
    unittest.main()
