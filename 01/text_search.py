import re
from typing import IO, Sequence


def grep(file: str | IO, words: Sequence[str]) -> str:
    with open(file, 'r', encoding='UTF-8') if isinstance(file, str) else file as file_obj:
        for line in file_obj:
            found = False
            for word in words:
                pattern = re.compile(rf'\b{word}\b', re.IGNORECASE)
                if re.search(pattern, line):
                    found = True
                    break
            if found:
                yield line


if __name__ == '__main__':
    with open('input/text1.txt', 'r', encoding='UTF-8') as f:
        print(list(grep(f, '')))
