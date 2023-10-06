# Домашнее задание #02 (функции, декораторы)

## Формулировка задачи

---
### 1. Реализовать класс CustomList наследованием от list

При этом:
- CustomList должен наследоваться от встроенного списка `list`;
- экземпляры CustomList можно складывать друг с другом и с обычными списками:
  ```py
  CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7])  # CustomList([6, 3, 10, 7])
  CustomList([1]) + [2, 5]  # CustomList([3, 5])
  [2, 5] + CustomList([1])  # CustomList([3, 5])
  ```
- экземпляры CustomList поддерживают вычитание между собой и с обычными списками:
  ```py
  CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7])  # CustomList([4, -1, -4, 7])
  CustomList([1]) - [2, 5]  # CustomList([-1, -5])
  [2, 5] - CustomList([1])  # CustomList([1, 5])
  ```
- результатом сложения/вычитания должен быть новый кастомный список;
- при сложении/вычитании списков разной длины отсутствующие элементы меньшего списка считаются нулями;
- при сложения/вычитания исходные списки должны оставаться неизменными;
- при сравнении (==, !=, >, >=, <, <=) экземпляров CustomList должна сравниваться сумма элементов списков (сравнение с list не нужно);
- должен быть переопределен str, чтобы выводились элементы списка и их сумма;
- списки можно считать всегда числовыми.


## Решение

---

### Описание решения


Задание реализовано в файле `custom_list.py`. Тесты к нему находятся в файле `test_custom_list.py`.

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
python3 -m unittest discover 03/
```

### Отчет линтеров

1. **Pylint**
```bash
(deep_python) mikhail_ovakimyan@192 deep_python_hw % pylint 03/
************* Module test_custom_list
03/test_custom_list.py:7:4: C0103: Method name "assertCustomListEqual" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:91:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:91:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:121:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:121:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:145:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:145:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:169:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:169:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:174:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:174:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:178:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:178:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:182:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:182:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:186:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:186:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:190:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:190:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:194:8: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:194:11: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
03/test_custom_list.py:34:0: R0904: Too many public methods (32/20) (too-many-public-methods)

------------------------------------------------------------------
Your code has been rated at 8.84/10 (previous run: 8.32/10, +0.52)

```

**Пояснения**:
1. Ошибка, связанная с методом `assertCustomListEqual`, допущена осознанно, чтобы метод не выделялся на фоне аналогичных из unittest
2. Переменные x и y были использованны в однотипных тестах, чтобы улучшить читаемость кода
3. Ошибка "Too many public methods" тоже игнорируется, так как это класс тестов


2. **Flake8**
```bash
flake8 03/
```

