from cProfile import Profile
from typing import Callable, Any


def profile_deco(func: Callable) -> Callable:
    class ProfiledFunc:
        def __init__(self):
            self.profiler = Profile()

        def __call__(self, *args, **kwargs) -> Any:
            with self.profiler:
                result = func(*args, **kwargs)

            return result

        def print_stat(self):
            self.profiler.print_stats()

    return ProfiledFunc()


if __name__ == '__main__':
    @profile_deco
    def add(a, b):
        return a + b

    @profile_deco
    def sub(a, b):
        return a - b

    for _ in range(10**6):
        add(1, 2)
        add(4, 5)
        sub(4, 5)

    add.print_stat()
    sub.print_stat()
