import argparse
from memory_profiler import profile
from time_comparison import (IntClass, StrClass, DictClass, DefaultAttrsClass,
                             SlotsAttrsClass, WeakrefAttrsClass)


@profile
def time_instantiation(cls, repeats=10**7):
    integer, string, dictionary = (
        IntClass(10), StrClass('10'), DictClass({'10': 10}))
    objs = [cls(integer, string, dictionary) for _ in range(repeats)]

    return objs


@profile
def time_reading(objs):
    _ = [obj.int_attr for obj in objs]


@profile
def time_writing(objs):
    integer, string, dictionary = (
        IntClass(20), StrClass('20'), DictClass({'20': 20}))

    for obj in objs:
        obj.int_attr = integer
        obj.str_attr = string
        obj.dict_attr = dictionary


if __name__ == '__main__':
    classes = {
        'default': DefaultAttrsClass,
        'slots': SlotsAttrsClass,
        'weakref': WeakrefAttrsClass
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str)
    args = parser.parse_args()

    objects = time_instantiation(classes[args.c], repeats=10 ** 6)
    time_reading(objects)
    time_writing(objects)
