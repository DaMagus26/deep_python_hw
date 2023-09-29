import json
from typing import Sequence, Optional, Callable


def parse_json(
        json_str: str,
        required_fields: Optional[Sequence] = None,
        keywords: Optional[Sequence] = None,
        keyword_callback: Optional[Callable] = None) -> None:
    required_fields = required_fields or []
    keywords = keywords or []
    keyword_callback = keyword_callback or (lambda x: ...)

    json_data = json.loads(json_str)
    for field in required_fields:
        value = json_data.get(field)
        if value:
            for kw in keywords:
                if kw in value.split():
                    keyword_callback(kw)


if __name__ == '__main__':
    input_str = '{"key1": "word1 word2", "key2": "word3 word4"}'
    parse_json(
        input_str,
        required_fields=['key2'],
        keywords=['word3'],
        keyword_callback=(lambda x: print(x)))
