# Домашнее задание #05 (стандартная библиотека)

## Формулировка задачи

---
### 1. LRU-кэш
Интерфейс:

```py
    class LRUCache:

        def __init__(self, limit=42):
            pass

        def get(self, key):
            pass

        def set(self, key, value):
            pass


    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


    Если удобнее, get/set можно сделать по аналогии с dict:
    cache["k1"] = "val1"
    print(cache["k3"])
```

Сложность решения по времени в среднем должна быть константной O(1).
Реализация любым способом без использования OrderedDict.

## Решение

---

### Описание решения


Задание реализовано в файле `lru_cache.py`. Тесты к нему находятся в файле `test_lru_cache.py`.

Перед проверкой задания необходимо установить все используемые модули:
```bash
pip install -r requirements.txt
```

Исходная конфигурация pylint была изменена. Необходимо подключить новый конфигурационный файл:
```bash
pylint --rcfile .pylintrc
```

### Запуск тестов

Для запуска тестов для обоих заданий необходимо выполнить следующую команду:
```bash
python3 -m unittest discover 05/
```

### Отчет линтеров

**Pylint**
```bash
(deep_python) mikhail_ovakimyan@192 deep_python_hw % pylint 05/

-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 9.55/10, +0.45)

```

**Flake8**
```bash
flake8 05/
```

