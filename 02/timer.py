from typing import Callable
from time import time


class AvgExecTime:
    def __init__(self, repeats: int = 10):
        if repeats < 1:
            raise ValueError(f"Number of repeats must be at least 1 ({repeats=})")

        self.repeats = repeats
        self.buffer = []

    def __call__(self, func: Callable) -> Callable:
        def function(*args, **kwargs):
            start_time = time()
            result = func(*args, **kwargs)
            execution_time = time() - start_time

            if len(self.buffer) == self.repeats:
                mean_time = sum(self.buffer) / self.repeats
                print(f"Wall time for {self.repeats} last calls: {mean_time:0.3f}")
                del self.buffer[0]
                self.buffer.append(execution_time)
            elif len(self.buffer) < self.repeats:
                self.buffer.append(execution_time)
            else:
                raise OverflowError()

            return result

        return function


if __name__ == '__main__':
    @AvgExecTime(repeats=3)
    def test_func(text):
        print(text)

    for _ in range(6):
        test_func('text')


