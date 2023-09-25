import re
from typing import IO


def grep(file: str | IO, word: str) -> str:
    pattern = re.compile(rf'\b{word}\b', re.IGNORECASE)

    with open(file, 'r', encoding='UTF-8') if isinstance(file, str) else file:
        for line in file.readlines():
            if re.search(pattern, line):
                yield line


if __name__ == '__main__':
    with open('input/text1.txt', 'r', encoding='UTF-8') as f:
        print(list(grep(f, '')))
