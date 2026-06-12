# 🎯 Урок 11: Lambda-функции и встроенные функции

## 📖 Теория

Lambda-функции — анонимные однострочные функции. Встроенные функции высшего порядка (`map`, `filter`, `reduce`, `sorted`, `any`, `all`) позволяют писать функциональный код без явных циклов.

---

## 🔹 Lambda-функции

```python
# Синтаксис: lambda аргументы: выражение
square = lambda x: x ** 2
add = lambda a, b: a + b
get_name = lambda obj: obj["name"]
```

**Когда использовать:**
- Простая функция в одну строку
- Передача в `map`/`filter`/`sorted`/`key`
- Не нужна повторно

**Когда НЕ использовать:**
- Сложная логика (> 1 строки) — используйте `def`
- Нужна документация — используйте `def`
- Содержит операторы (`if`, `for`, `try`) — нельзя в lambda!

---

## 🔹 `map()` — применение функции к каждому элементу

```python
# Без map
result = []
for x in range(5):
    result.append(x ** 2)

# С map
result = list(map(lambda x: x ** 2, range(5)))  # [0, 1, 4, 9, 16]

# Несколько итераторов
a = [1, 2, 3]
b = [10, 20, 30]
list(map(lambda x, y: x + y, a, b))  # [11, 22, 33]

# С обычной функцией
def to_celsius(f):
    return (f - 32) * 5 / 9
temps_f = [32, 68, 104]
temps_c = list(map(to_celsius, temps_f))  # [0.0, 20.0, 40.0]

# ✅ map быстрее, чем list comprehension для простых операций с встроенными функциями
list(map(str.upper, ["a", "b", "c"]))  # Быстрее, чем [...]
```

---

## 🔹 `filter()` — фильтрация по условию

```python
numbers = [1, -2, 3, -4, 5, -6]

# Только положительные
positive = list(filter(lambda x: x > 0, numbers))  # [1, 3, 5]

# Только правдивые значения
data = [0, "", "hello", None, [], "world", False]
truthy = list(filter(None, data))  # ["hello", "world"]

# Комбинация с map
even_squares = list(map(
    lambda x: x ** 2,
    filter(lambda x: x % 2 == 0, range(10))
))  # [0, 4, 16, 36, 64]
```

---

## 🔹 `reduce()` — свёртка последовательности

```python
from functools import reduce

# Сумма всех элементов
reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)  # 10

# Произведение (факториал)
reduce(lambda acc, x: acc * x, range(1, 6))  # 120

# Максимум
reduce(lambda a, b: a if a > b else b, [3, 1, 4, 1, 5])  # 5

# Конкатенация строк
reduce(lambda acc, s: acc + " " + s, ["Hello", "World"])  # "Hello World"
```

---

## 🔹 `sorted()` — сортировка

```python
users = [
    {"name": "Борис", "age": 35},
    {"name": "Анна", "age": 28},
    {"name": "Вера", "age": 22},
]

# По ключу
sorted(users, key=lambda u: u["age"])      # По возрасту
sorted(users, key=lambda u: u["name"])      # По имени

# По длине
words = ["python", "is", "awesome"]
sorted(words, key=len)  # ["is", "python", "awesome"]

# По убыванию
sorted(words, key=len, reverse=True)

# Несколько ключей (кортеж)
data = [(1, 3), (2, 2), (1, 1), (2, 1)]
sorted(data, key=lambda x: (x[0], x[1]))  # Сначала по первому, потом по второму
```

---

## 🔹 `any()` / `all()` — проверка коллекций

```python
# any — True если хотя бы один True
any([False, True, False])      # True
any([False, False, False])     # False
any([])                         # False (пустая коллекция)

# all — True если все True
all([True, True, True])         # True
all([True, False, True])        # False
all([])                         # True (пустая коллекция — все True!)

# Практические примеры
nums = [2, 4, 6, 8]
all(n % 2 == 0 for n in nums)   # True (все чётные)
any(n > 5 for n in nums)        # True (есть > 5)

# Проверка на None
values = [1, 2, None, 4]
all(v is not None for v in values)  # False
```

---

## 🔹 Другие полезные встроенные функции

```python
# zip — параллельная итерация
list(zip([1, 2, 3], "abc"))  # [(1, 'a'), (2, 'b'), (3, 'c')]

# enumerate — счётчик
list(enumerate("abc", start=1))  # [(1, 'a'), (2, 'b'), (3, 'c')]

# max/min с key
max(users, key=lambda u: u["age"])  # {"name": "Борис", "age": 35}

# sum с начальным значением
sum(range(5), 100)  # 110 (0+1+2+3+4+100)

# isinstance — проверка типа
isinstance(42, int)       # True
isinstance("hi", (int, str))  # True

# hasattr, getattr, setattr
hasattr(user, "name")
getattr(user, "name", "Unknown")
```

---

## 🔹 `itertools` — продвинутые итераторы

```python
import itertools

# count — бесконечный счётчик
for i in itertools.count(start=10, step=2):
    if i > 20: break  # 10, 12, 14, 16, 18, 20

# cycle — бесконечный цикл
colors = itertools.cycle(["red", "green", "blue"])
[next(colors) for _ in range(5)]  # ['red', 'green', 'blue', 'red', 'green']

# repeat — повторение
list(itertools.repeat("A", 3))  # ['A', 'A', 'A']

# chain — сцепление итераторов
list(itertools.chain([1, 2], [3, 4], "ab"))  # [1, 2, 3, 4, 'a', 'b']

# combinations / permutations
list(itertools.combinations("ABC", 2))   # [('A','B'), ('A','C'), ('B','C')]
list(itertools.permutations("AB", 2))     # [('A','B'), ('B','A')]

# product — декартово произведение
list(itertools.product("AB", [1, 2]))    # [('A',1), ('A',2), ('B',1), ('B',2)]

# groupby — группировка
data = [("a", 1), ("a", 2), ("b", 3)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# a [('a', 1), ('a', 2)]
# b [('b', 3)]
```

---

## 🧪 Упражнения

1. Используя `map` и `filter`, получите список квадратов чётных чисел от 1 до 20
2. Реализуйте `flatten(nested)` с помощью `reduce` и `itertools.chain`
3. Напишите проверку: все ли слова в предложении длиннее 3 символов (используйте `all`)
4. Сгенерируйте все возможные комбинации броска двух кубиков с помощью `itertools.product`
