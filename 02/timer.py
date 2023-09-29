from typing import Callable, Optional, Literal
from time import time, sleep


def mean(repeats: int = 10):
    if repeats < 1:
        raise ValueError(f'Number of repeats must be at least 1 ({repeats=})')

    def _mean_inner(func: Callable) -> Callable:
        def function(*args, **kwargs):
            start_time = time()
            result = None

            for _ in range(repeats):
                result = func(*args, **kwargs)

            wall_time = (time() - start_time) / repeats

            # if output:
            print(f'Wall time: {wall_time:0.3f}')

            return result

        return function
    return _mean_inner
