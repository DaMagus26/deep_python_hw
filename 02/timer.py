from typing import Callable
from time import time, sleep


def mean(repeats=10):
    def _mean_inner(func: Callable) -> Callable:
        def function(*args, **kwargs):
            start_time = time()
            result = None

            for _ in range(repeats):
                result = func(*args, **kwargs)

            wall_time = (time() - start_time) / repeats

            print(f'Wall time: {wall_time:0.3f}')
            return result

        return function
    return _mean_inner


if __name__ == '__main__':
    @mean(10)
    def chill(text):
        sleep(1)
        print(text)

    chill('Hello, world!')
