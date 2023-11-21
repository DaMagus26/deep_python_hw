import logging
import logging.config
import os
import argparse
from typing import Dict, Any, Optional


class LRUCache:
    def __init__(
            self,
            max_size: int,
            logger: logging.Logger,
    ) -> None:
        if max_size < 1:
            raise ValueError('"max_size" must be equal'
                             f' or greater than 1 ({max_size=})')
        if not isinstance(max_size, int):
            raise TypeError('"max_size" must be an integer')

        self.__max_size: int = max_size
        self.__data: Dict = {}
        self.__logger: logging.Logger = logger
        self.__logger.debug('LRU cache initiated')

    def __getitem__(self, item: Any) -> Any:
        element = self.__data.get(item, None)
        if element is not None:
            del self.__data[item]
            self.__data[item] = element
            self.__logger.debug(
                "getting existing element: %s",
                element,
            )
        else:
            self.__logger.info('getting non-existing element')

        return element

    def __setitem__(self, key, value) -> None:
        element = self.__data.get(key, None)
        if element is None:
            self.__logger.debug(
                "setting non-existing element: %s",
                value)
            if len(self.__data) >= self.__max_size:
                self.__logger.warning(
                    "cache max capacity is reached")
                first_element_idx = next(iter(self.__data.keys()))
                del self.__data[first_element_idx]
        else:
            self.__logger.debug(
                "setting existing element: %s",
                value)
            del self.__data[key]
            self.__data[key] = value

        self.__data[key] = value

    @property
    def state(self) -> Dict:
        return self.__data


class CustomFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return len(record.msg) > 10


def setup_logger(
        file_path: str,
        stdout: Optional[bool] = False,
) -> logging.Logger:
    # Validating input
    file_path = file_path.strip()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Setting up file handler
    file_handler = logging.FileHandler(file_path, 'w')
    file_formatter = logging.Formatter('%(asctime)s [%(name)s:%(levelname)s] %(message)s')
    file_handler.addFilter(CustomFilter())
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # Setting up stdout handler if needed
    if stdout:
        stdout_handler = logging.StreamHandler()
        stdout_formatter = logging.Formatter('%(name)-8s %(message)s (%(levelname)s)')
        stdout_handler.setFormatter(stdout_formatter)
        stdout_handler.setLevel(logging.DEBUG)
        logger.addHandler(stdout_handler)

    return logger


def run_test(args):
    logger = setup_logger(args.filepath, args.stdout)
    cache = LRUCache(2, logger)
    
    cache["k1"] = "val1"
    cache["k2"] = "val2"
    
    assert cache["k3"] is None
    assert cache["k2"] == "val2"
    assert cache["k1"] == "val1"
    
    cache["k3"] = "val3"
    
    assert cache["k3"] == "val3"
    assert cache["k2"] is None
    assert cache["k1"] == "val1"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stdout', action='store_true')
    parser.add_argument('-f', '--filepath', type=str, default='cache.log')
    args = parser.parse_args()

    run_test(args)
