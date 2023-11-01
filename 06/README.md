# Домашнее задание #06 (многопоточные приложения)

## Формулировка задачи

---
### 1. Клиент-серверное приложение для обкачки набора урлов с ограничением нагрузки
#### Cервер
master-worker cервер для обработки запросов от клиента.

Алгоритм должен быть следующим:

    - Сервер должен поддерживать взаимодействие с любым числом клиентов;
    - Мастер и воркеры это разные потоки в едином приложении сервера;
    - Количество воркеров задается при запуске;
    - Мастер слушает порт, на который клиенты будут по TCP отправлять урлы для обкачки;
    - Мастер принимает запроc и передает его одному из воркеров;
    - Воркер читает url от клиента;
    - Воркер обкачивает url по http и возвращает клиенту топ K самых частых слов и их частоту в формате json {"word1": 10, "word2": 5};
    - После каждого обработанного урла сервер должен вывести статистику: сколько урлов было обработано на данный момент суммарно всеми воркерами;

`python server.py -w 10 -k 7` (сервер использует 10 воркеров для обкачки и отправляет клиенту топ-7 частых слов)

#### Клиент
Утилита, отправляющая запросы с урлами серверу по TCP в несколько потоков.
Нужно сделать следующее:

    - Подготовить файл с запросами (порядка 100 разных url);
    - На вход клиенту передаётся два аргумента --- файл с URL'ами и количество потоков M;
    - Клиент создает M потоков, отправляет запросы на сервер в каждом потоке и печатает ответ сервера в стандартый вывод, например: `xxx.com: {'word1': 100, 'word2': 50}`.

`python client.py 10 urls.txt`


## Решение

---

### Описание решения


Сервер реализован в файле `server.py`. Тесты к нему находятся в файле `test_server.py`. Клиент реализован в файле `client.py`. Тесты к нему находятся в файле `test_client.py`.

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
python3 -m unittest discover 06/
```

### Отчет линтеров

**Pylint**
```text
(deep_python_hw) mikhail_ovakimyan@192 deep_python_hw % pylint 06/
************* Module server
06/server.py:16:4: R0913: Too many arguments (6/5) (too-many-arguments)
06/server.py:52:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
06/server.py:56:24: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
06/server.py:91:15: W0718: Catching too general exception Exception (broad-exception-caught)
06/server.py:82:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
06/server.py:86:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
06/server.py:92:12: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
************* Module client
06/client.py:48:19: W0718: Catching too general exception Exception (broad-exception-caught)
06/client.py:49:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
************* Module test_server
06/test_server.py:52:17: W0212: Access to a protected member _most_common_words of a client class (protected-access)
06/test_server.py:61:17: W0212: Access to a protected member _most_common_words of a client class (protected-access)
06/test_server.py:91:8: W0212: Access to a protected member _process_connection of a client class (protected-access)
06/test_server.py:92:25: W0212: Access to a protected member _total_processed of a client class (protected-access)
06/test_server.py:109:8: W0212: Access to a protected member _process_connection of a client class (protected-access)
06/test_server.py:110:25: W0212: Access to a protected member _total_processed of a client class (protected-access)
06/test_server.py:125:8: W0212: Access to a protected member _process_connection of a client class (protected-access)
06/test_server.py:126:25: W0212: Access to a protected member _total_processed of a client class (protected-access)
************* Module test_client
06/test_client.py:70:12: W0212: Access to a protected member _partition_list of a client class (protected-access)
06/test_client.py:73:12: W0212: Access to a protected member _partition_list of a client class (protected-access)
06/test_client.py:76:12: W0212: Access to a protected member _partition_list of a client class (protected-access)
06/test_client.py:79:12: W0212: Access to a protected member _partition_list of a client class (protected-access)
06/test_client.py:82:16: W0212: Access to a protected member _partition_list of a client class (protected-access)

------------------------------------------------------------------
Your code has been rated at 9.19/10 (previous run: 9.15/10, +0.04)
```

*Примечание*: предупреждения о доступе к защищенным методам проигнорированы, т.к. это необходимо для тестирования.

Предупреждения broad-exception-caught так же проигнорированы, так как после поимки Exception поток сразу же завершается.

**Flake8**
```bash
flake8 06/
```

