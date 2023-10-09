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

**Pylint**
```bash
(deep_python) mikhail_ovakimyan@192 deep_python_hw % pylint 04/
************* Module test_descriptors
04/test_descriptors.py:16:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:24:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:32:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:40:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:48:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:56:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:72:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:80:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:88:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:96:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:107:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:115:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:126:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:134:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:145:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:153:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:169:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:177:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:185:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:193:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:201:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
04/test_descriptors.py:209:8: C0103: Variable name "db" doesn't conform to snake_case naming style (invalid-name)
************* Module test_custom_metaclass
04/test_custom_metaclass.py:25:25: E1101: Class 'Example' has no 'custom_attr' member (no-member)
04/test_custom_metaclass.py:35:25: E1101: Class 'Example' has no 'custom_func' member (no-member)
04/test_custom_metaclass.py:55:8: W0201: Attribute 'attr' defined outside __init__ (attribute-defined-outside-init)
04/test_custom_metaclass.py:58:25: E1101: Instance of 'Example' has no 'custom_attr' member (no-member)
04/test_custom_metaclass.py:69:25: E1101: Instance of 'Example' has no 'custom_attr' member (no-member)
04/test_custom_metaclass.py:76:8: W0201: Attribute 'attr' defined outside __init__ (attribute-defined-outside-init)
04/test_custom_metaclass.py:79:25: E1101: Instance of 'Example' has no 'custom_attr' member (no-member)
04/test_custom_metaclass.py:87:12: W0246: Useless parent or super() delegation in method '__init__' (useless-parent-delegation)
04/test_custom_metaclass.py:93:25: E1101: Instance of 'ExampleChild' has no 'custom_attr' member (no-member)
04/test_custom_metaclass.py:101:8: W0201: Attribute 'attr' defined outside __init__ (attribute-defined-outside-init)
04/test_custom_metaclass.py:106:25: E1101: Instance of 'Example' has no 'new_custom_attr' member (no-member)

------------------------------------------------------------------
Your code has been rated at 8.15/10 (previous run: 8.10/10, +0.05)
```

**Пояснения**:
1. Переменные db были использованны в однотипных тестах, чтобы улучшить читаемость кода
2. Ошибки, связанные с объявлением атрибутов за пределами объявления класса игнорируются, так как их решение противоречит сути задания.

**Flake8**
```bash
flake8 04/
```

