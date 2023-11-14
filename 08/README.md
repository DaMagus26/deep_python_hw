# Домашнее задание #08 (память, профилирование)

## Формулировка задачи

---

### 1. Сравнение использования weakref и слотов
Нужно придумать свои типы с несколькими атрибутами:
- класс с обычными атрибутами
- класс со слотами
- класс с атрибутами weakref

Для каждого класса создается большое число экземпляров и замеряется (сравнивается):
- время создания пачки экземпляров
- время чтения/изменения атрибутов

Результаты замеров оформляются скриншотами c описанием и выводом.

### 2. Профилирование
Провести профилирование вызовов и памяти для кода из пункта 1.

Результаты оформляются скриншотами c описанием.

### 3. Декоратор для профилирования
Применение декоратора к функции должно выполнять прoфилирование (cProfile) всех вызовов данной функции.
Вызов метода `.print_stat()` должен выводить единую таблицу со статистикой профилирования суммарно по всем вызовам функции.


```py
def profile_deco(...):
    ...


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)


add.print_stat()  # выводится результат профилирования суммарно по всем вызовам функции add (всего два вызова)
sub.print_stat()  # выводится результат профилирования суммарно по всем вызовам функции sub (всего один вызов)
```

### 4. Перед отправкой на проверку код должен быть прогнан через flake8 и pylint, по желанию еще black

## Решение

---

### Описание решения


Замер времени работы классов и сами классы реализованы в `time_comparison.py`.

Их профилирование выполняется из файла `profiling.py`. Для запуска введите:
```shell
python3 08/profiling.py -c <type>
```
где `<type>` = `default` / `slots` / `weakref` для профилирования соответствующих им классов.

Кастомный декоратор для профилирования находтся в `profiler_decorator.py`.


### Конфигурация

Перед проверкой задания необходимо установить все используемые модули:
```bash
pip install -r requirements.txt
```

Исходная конфигурация pylint была изменена. Необходимо подключить новый конфигурационный файл:
```bash
pylint --rcfile .pylintrc
```

### Результаты запусков
#### Время заполнения

Время заполнения, чтения и записи аттрибутов классов DefaultAttrClass, SlotsAttrClass, WeakrefAttrClass для 10 млн итераций.

![time.png](images%2Ftime.png)

Заметно, что на время инициализации заметно дольше для WeakrefAttrClass. Вероятно из-за необходимости создавать новые сущности в init.

Время чтения меньше у SlotsAttrClass. Время записи между классами отличается незначительно.

#### Профилирование

Ниже приведены скрины для профилирования незначительно измененнных функций из `time_comparison.py`. Скрины приведены для DefaultAttrClass, SlotsAttrClass, WeakrefAttrClass соответственно

DefaultAttrClass
![profiler_default.png](images%2Fprofiler_default.png)

SlotsAttrClass
![profiler_slots.png](images%2Fprofiler_slots.png)

WeakrefAttrClass
![profiler_weakref.png](images%2Fprofiler_weakref.png)

По результатам профилирования видно, что операции над SlotsAttrClass требуют значительно меньше памяти, чем остальные. Остальные два класса отличаются друг от друга незначительно.

### Отчет линтеров

**Pylint**
```text
pylint 08/
************* Module profiler_decorator
08/profiler_decorator.py:24:12: C0103: Argument name "a" doesn't conform to snake_case naming style (invalid-name)
08/profiler_decorator.py:24:15: C0103: Argument name "b" doesn't conform to snake_case naming style (invalid-name)
08/profiler_decorator.py:29:12: C0103: Argument name "a" doesn't conform to snake_case naming style (invalid-name)
08/profiler_decorator.py:29:15: C0103: Argument name "b" doesn't conform to snake_case naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 9.64/10 (previous run: 8.45/10, +1.18)

```

**Flake8**
```bash
flake8 08/
```

