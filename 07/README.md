# Домашнее задание #07 (асинхронная обработка)

## Формулировка задачи

---
### Скрипт для асинхронной обкачки урлов
Написать скрипт для обкачки списка урлов с возможностью задавать количество одновременных запросов, используя асинхронное программирование.
Клиент можно использовать любой, например, из aiohttp.
Например, 10 одновременных запросов могут задаваться командой:

`python fetcher.py -c 10 urls.txt`
или
`python fetcher.py 10 urls.txt`

## Решение

---

### Описание решения


Скрипт реализован в файле `fetcher.py`. Тесты к нему находятся в файле `test_utils.py` и `test_async_fetcher.py`.

Запуск производится командой:
```bash
python 07/fetcher.py -c 10 -p 07/urls.txt
```

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
python3 -m unittest discover 07/
```

### Отчет линтеров

**Pylint**
```text
(deep_python_hw) mikhail_ovakimyan@192 deep_python_hw % pylint 07/
************* Module fetcher
07/fetcher.py:22:8: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)

------------------------------------------------------------------
Your code has been rated at 9.91/10 (previous run: 9.64/10, +0.27)

```

**Flake8**
```bash
flake8 07/
```

