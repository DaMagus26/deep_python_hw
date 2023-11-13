import unittest
from unittest import mock
from custom_metaclass import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def test_isinstance(self):
        class Example(metaclass=CustomMeta):
            pass

        self.assertIsInstance(Example, CustomMeta)

    def test_setattr(self):
        class Example(metaclass=CustomMeta):
            pass

        self.assertIn('__setattr__', Example.__dict__)

    def test_initial_attr_has_prefix(self):
        class Example(metaclass=CustomMeta):
            attr = 10

        self.assertIn('custom_attr', Example.__dict__)
        self.assertNotIn('attr', Example.__dict__)
        self.assertEqual(Example.custom_attr, 10)

    def test_initial_func_has_prefix(self):
        class Example(metaclass=CustomMeta):
            @staticmethod
            def func():
                return 10

        self.assertIn('custom_func', Example.__dict__)
        self.assertNotIn('func', Example.__dict__)
        self.assertEqual(Example.custom_func(), 10)

    def test_does_not_affect_dunder(self):
        class Example(metaclass=CustomMeta):
            def __init__(self):
                pass

        self.assertIn('__init__', Example.__dict__)
        self.assertNotIn('custom___init__', Example.__dict__)

    def test_does_not_affect_builtin_setattr(self):
        mock_func = mock.Mock()
        mock_func.return_value = 10

        class Example(metaclass=CustomMeta):
            def __setattr__(self, key, value):
                new_value = mock_func()
                self.__dict__[key] = new_value

        ex = Example()
        ex.attr = 20
        self.assertIn('custom_attr', ex.__dict__)
        self.assertNotIn('attr', ex.__dict__)
        self.assertEqual(ex.custom_attr, 10)
        self.assertEqual(mock_func.call_count, 1)

    def test_affects_instance_attrs(self):
        class Example(metaclass=CustomMeta):
            def __init__(self):
                self.attr = 10

        ex = Example()
        self.assertIn('custom_attr', ex.__dict__)
        self.assertNotIn('attr', ex.__dict__)
        self.assertEqual(ex.custom_attr, 10)

    def test_instance_affects_attrs_added_later(self):
        class Example(metaclass=CustomMeta):
            pass

        ex = Example()
        ex.attr = 10
        self.assertIn('custom_attr', ex.__dict__)
        self.assertNotIn('attr', ex.__dict__)
        self.assertEqual(ex.custom_attr, 10)

    def test_inherited_class(self):
        class ExampleParent:
            def __init__(self):
                self.attr = 10

        class ExampleChild(ExampleParent, metaclass=CustomMeta):
            def __init__(self):
                super().__init__()

        ex = ExampleChild()
        self.assertIn('custom_attr', ex.__dict__)
        self.assertNotIn('attr', ex.__dict__)
        self.assertEqual(ex.custom_attr, 10)

    def test_setattr_prefix_order(self):
        class Example(metaclass=CustomMeta):
            def __setattr__(self, key, value):
                self.__dict__['new_' + key] = value

        ex = Example()
        ex.attr = 10
        self.assertIn('new_custom_attr', ex.__dict__)
        self.assertNotIn('attr', ex.__dict__)
        self.assertNotIn('custom_attr', ex.__dict__)
        self.assertNotIn('new_attr', ex.__dict__)
        self.assertEqual(ex.new_custom_attr, 10)

    def test_adding_magic_methods_when_setattr_undefined(self):
        class Example(metaclass=CustomMeta):
            pass

        ex = Example()
        ex.__magic__ = 10
        self.assertIn('__magic__', ex.__dict__)
        self.assertNotIn('custom___attr__', ex.__dict__)
        self.assertEqual(ex.__magic__, 10)

    def test_adding_magic_methods_when_setattr_defined(self):
        class Example(metaclass=CustomMeta):
            def __setattr__(self, key, value):
                self.__dict__['new_' + key] = value

        ex = Example()
        ex.__magic__ = 10
        self.assertIn('new___magic__', ex.__dict__)
        self.assertNotIn('custom___magic__', ex.__dict__)
        self.assertNotIn('new_custom___magic__', ex.__dict__)
        self.assertEqual(ex.new___magic__, 10)

    def test_str(self):
        class Example(metaclass=CustomMeta):
            def __str__(self):
                return 'Custom_by_metaclass'

        ex = Example()
        self.assertEqual(str(ex), 'Custom_by_metaclass')


if __name__ == '__main__':
    unittest.main()
