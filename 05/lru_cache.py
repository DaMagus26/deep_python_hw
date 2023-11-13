from typing import Dict, Any

# Если верить https://stackoverflow.com/questions/39219065/
# операция dict().keys() имеет сложность O(1)


class LRUCache:
    def __init__(self, max_size: int) -> None:
        if max_size < 1:
            raise ValueError('"max_size" must be equal'
                             f' or greater than 1 ({max_size=})')
        if not isinstance(max_size, int):
            raise TypeError('"max_size" must be an integer')

        self.__max_size: int = max_size
        self.__data: Dict = {}

    def __getitem__(self, item: Any) -> Any:
        element = self.__data.get(item, None)  # Сложность O(1)
        if element is not None:
            del self.__data[item]  # Сложность O(1)
            self.__data[item] = element
        return element

    def __setitem__(self, key, value) -> None:
        element = self.__data.get(key, None)
        if element is None:
            if len(self.__data) >= self.__max_size:
                # Если судить по реализации ф-ции iter(),
                # она не проходит по всему массиву, а лишь создает
                # указатель на его первый элемент.
                # next просто вернет значение этого указателя
                # Тогда сложность получения последнего эл-та - O(1)
                # dict.keys() – в Python 3 тоже O(1)
                first_element_idx = next(iter(self.__data.keys()))
                del self.__data[first_element_idx]  # O(1)
        else:
            del self.__data[key]  # Сложность O(1)
            self.__data[key] = value

        self.__data[key] = value

    @property
    def state(self) -> Dict:
        return self.__data


if __name__ == '__main__':
    cache = LRUCache(2)

    cache["k1"] = "val1"
    cache["k2"] = "val2"

    assert cache["k3"] is None
    assert cache["k2"] == "val2"
    assert cache["k1"] == "val1"

    cache["k3"] = "val3"

    assert cache["k3"] == "val3"
    assert cache["k2"] is None
    assert cache["k1"] == "val1"
