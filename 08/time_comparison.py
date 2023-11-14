import weakref
import time


class IntClass:
    def __init__(self, value):
        self.value = value


class StrClass:
    def __init__(self, value):
        self.value = value


class DictClass:
    def __init__(self, value):
        self.value = value


class DefaultAttrsClass:
    def __init__(self, int_attr, str_attr, dict_attr):
        self.int_attr = int_attr
        self.str_attr = str_attr
        self.dict_attr = dict_attr


class SlotsAttrsClass:
    __slots__ = ('int_attr', 'str_attr', 'dict_attr')

    def __init__(self, int_attr, str_attr, dict_attr):
        self.int_attr = int_attr
        self.str_attr = str_attr
        self.dict_attr = dict_attr


class WeakrefAttrsClass:
    def __init__(self, int_attr, str_attr, dict_attr):
        self.int_attr = weakref.ref(int_attr)
        self.str_attr = weakref.ref(str_attr)
        self.dict_attr = weakref.ref(dict_attr)


def time_instantiation(cls, repeats=10**7):
    integer, string, dictionary = (
        IntClass(10), StrClass('10'), DictClass({'10': 10}))
    start_time = time.perf_counter()
    objs = [cls(integer, string, dictionary) for _ in range(repeats)]
    exec_time = time.perf_counter() - start_time

    return objs, exec_time


def time_reading(objs):
    start_time = time.perf_counter()
    _ = [obj.int_attr for obj in objs]
    exec_time = time.perf_counter() - start_time

    return exec_time


def time_writing(objs):
    integer, string, dictionary = (
        IntClass(20), StrClass('20'), DictClass({'20': 20}))

    start_time = time.perf_counter()
    for obj in objs:
        obj.int_attr = integer
        obj.str_attr = string
        obj.dict_attr = dictionary
    exec_time = time.perf_counter() - start_time

    return exec_time


if __name__ == '__main__':
    defaults, d_time = time_instantiation(
        DefaultAttrsClass, repeats=10**7)
    print(f'Wall time for instantiation a class with '
          f'default attributes: {d_time:.3f}')
    slots, s_time = time_instantiation(
        SlotsAttrsClass, repeats=10**7)
    print(f'Wall time for instantiation a class with '
          f'slots attributes: {s_time:.3f}')
    weakrefs, w_time = time_instantiation(
        WeakrefAttrsClass, repeats=10**7)
    print(f'Wall time for instantiation a class with '
          f'weakref attributes: {w_time:.3f}\n')

    defaults *= 10
    slots *= 10
    weakrefs *= 10
    print(f'Wall time for reading from class with '
          f'default attributes: {time_reading(defaults):.3f}')
    print(f'Wall time for reading from class with '
          f'slots attributes: {time_reading(slots):.3f}')
    print(f'Wall time for reading from class with '
          f'weakref attributes: {time_reading(weakrefs):.3f}\n')

    print(f'Wall time for writing to class with '
          f'default attributes: {time_writing(defaults):.3f}')
    print(f'Wall time for writing to class with '
          f'slots attributes: {time_writing(slots):.3f}')
    print(f'Wall time for writing to class with '
          f'weakref attributes: {time_writing(weakrefs):.3f}\n')
