# Домашнее задание #04 (метаклассы, дескрипторы)

## Формулировка задачи

---
### 1. Метакласс, который в начале названий всех атрибутов и методов, кроме магических, добавляет префикс "custom_"
  Подменяться должны атрибуты класса и атрибуты экземпляра класса, в том числе добавленные после выполнения конструктора (dynamic в примере).

```py
    class CustomMeta(...):
        pass


    class CustomClass(metaclass=CustomMeta):
        x = 50

        def __init__(self, val=99):
            self.val = val

        def line(self):
            return 100

        def __str__(self):
            return "Custom_by_metaclass"


    assert CustomClass.custom_x == 50
    CustomClass.x  # ошибка

    inst = CustomClass()
    assert inst.custom_x == 50
    assert inst.custom_val == 99
    assert inst.custom_line() == 100
    assert str(inst) == "Custom_by_metaclass"

    inst.x  # ошибка
    inst.val  # ошибка
    inst.line() # ошибка
    inst.yyy  # ошибка

    inst.dynamic = "added later"
    assert inst.custom_dynamic == "added later"
    inst.dynamic  # ошибка
```


### 2. Дескрипторы с проверками типов и значений данных
  Нужно сделать три дескриптора для какой-то области интереса (наука, финансы, хобби и тд), но если совсем не получается, то можно использовать шаблона ниже в качестве основы.

```py
    class Integer:
        pass

    class String:
        pass

    class PositiveInteger:
        pass

    class Data:
        num = Integer()
        name = String()
        price = PositiveInteger()

        def __init__(...):
            ....
```

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

