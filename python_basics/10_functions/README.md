# 🏗️ Урок 10: Функции в Python

## 📖 Теория

Функция — именованный блок кода, который можно переиспользовать. Основа модульности и абстракции в программировании.

---

## 🔹 Определение и вызов

```python
def имя_функции(параметр1, параметр2):
    """Документация (docstring)."""
    результат = параметр1 + параметр2
    return результат

# Вызов
result = имя_функции(3, 4)  # result = 7
```

---

## 🔹 Параметры и аргументы

### Типы параметров
```python
def func(a, b, c):          # Позиционные (обязательные)
    pass

def func(a, b=10, c=20):    # Со значениями по умолчанию
    pass

def func(*args, **kwargs):  # Произвольное количество
    pass

def func(a, b, *, c, d):    # Keyword-only (после *)
    pass

def func(a, b, /, c, d):    # Positional-only (до /) — Python 3.8+
    pass
```

### Порядок параметров
```python
def func(pos1, pos2, /, pos_or_kw, *, kw_only1, kw_only2):
    """
    pos1, pos2   — ТОЛЬКО позиционные (до /)
    pos_or_kw    — позиционные ИЛИ именованные
    kw_only1, kw_only2 — ТОЛЬКО именованные (после *)
    """
```

### `*args` и `**kwargs`
```python
# *args — кортеж позиционных аргументов
def sum_all(*args):
    return sum(args)
sum_all(1, 2, 3, 4)  # 10

# **kwargs — словарь именованных аргументов
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
print_info(name="Анна", age=28, city="Москва")

# Распаковка при вызове
def greet(name, age):
    print(f"{name}, {age} лет")

data = {"name": "Анна", "age": 28}
greet(**data)  # greet(name="Анна", age=28)

numbers = [1, 2, 3]
sum_all(*numbers)  # sum_all(1, 2, 3)
```

---

## 🔹 `return` и возврат значений

```python
# Одно значение
def double(x):
    return x * 2

# Несколько значений (на самом деле — кортеж!)
def min_max(lst):
    return min(lst), max(lst)
minimum, maximum = min_max([3, 1, 4, 1, 5])

# Без return — возвращает None
def noop():
    pass
result = noop()  # None

# Ранний выход
def safe_divide(a, b):
    if b == 0:
        return None         # Ранний выход
    return a / b
```

---

## 🔹 Области видимости (Scope)

```python
# LEGB правило: Local → Enclosing → Global → Built-in

x = "global"                   # Глобальная

def outer():
    x = "enclosing"            # Объемлющая (для inner)
    def inner():
        x = "local"            # Локальная
        print(x)               # "local"
    inner()
    print(x)                   # "enclosing"

print(x)                       # "global"

# global — изменить глобальную переменную
def set_global():
    global x
    x = "changed"

# nonlocal — изменить переменную из объемлющей функции
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
c = counter()
c()  # 1
c()  # 2
```

---

## 🔹 Лямбда-функции (анонимные)

```python
# Синтаксис: lambda аргументы: выражение
double = lambda x: x * 2
add = lambda a, b: a + b

# В сортировке
users.sort(key=lambda u: u["age"])

# С map/filter
list(map(lambda x: x**2, [1, 2, 3]))
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))
```

---

## 🔹 Рекурсия

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(5)  # 120

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

⚠️ В Python ограничение глубины рекурсии (`sys.getrecursionlimit()` ≈ 1000).

---

## 🔹 Декораторы (введение)

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__} с {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Результат: {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(3, 4)
# Вызов add с (3, 4), {}
# Результат: 7
```

---

## 🔹 Type Hints (аннотации типов)

```python
def greet(name: str, age: int) -> str:
    return f"{name}, {age} лет"

def process(data: list[int], config: dict[str, any] | None = None) -> bool:
    ...
```

---

## ⚠️ Частые ошибки

```python
# ❌ Изменяемый аргумент по умолчанию
def append_to(element, target=[]):
    target.append(element)
    return target

append_to(1)  # [1]
append_to(2)  # [1, 2] — ТОТ ЖЕ список! Не [2]!

# ✅ Правильно
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

# ❌ Смешивание позиционных и именованных
def f(a, b): pass
f(b=2, 1)  # SyntaxError: позиционный после именованного!

# ❌ Забытый return
def bad_func(x):
    x * 2          # Вычислено, но не возвращено!
result = bad_func(5)  # None
```

---

## 💡 Лучшие практики

1. **Одна функция — одна задача** (Single Responsibility)
2. **Имена функций — глаголы**: `calculate_total()`, `get_user()`, `is_valid()`
3. **Docstrings** для всех публичных функций
4. **Type hints** для улучшения читаемости и IDE-подсказок
5. **Не более 3-4 параметров**; если больше — используйте словарь или dataclass
6. **Ранний выход** вместо глубокой вложенности

---

## 🧪 Упражнения

1. Напишите функцию `is_palindrome(s)`, проверяющую, является ли строка палиндромом
2. Реализуйте рекурсивную функцию `binary_search(sorted_list, target)`
3. Создайте декоратор `@retry(n)`, повторяющий функцию до n раз при ошибке
4. Напишите функцию-генератор `chunks(lst, n)`, разбивающую список на куски размером n
