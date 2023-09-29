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
            for keyword in keywords:
                if keyword in value.split():
                    keyword_callback(keyword)
