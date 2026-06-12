# 🧠 Python Cheatsheet — шпаргалка

> Распечатай и повесь на стену. Здесь ВСЁ что нужно для ежедневной работы.

---

## 🔤 Базовый синтаксис

```python
# Переменные
name = "Анна"         # str — строка
age = 28              # int — целое
price = 19.99         # float — дробное
is_active = True      # bool — True/False
nothing = None        # NoneType — пустота

# Вывод
print("Привет", name)            # Привет Анна
print(f"{name}, {age} лет")     # f-строка: Анна, 28 лет

# Ввод
name = input("Как вас зовут? ")  # Всегда возвращает строку!
age = int(input("Возраст: "))    # Преобразование в число

# Узнать тип
type(42)        # <class 'int'>
isinstance(42, int)  # True
```

---

## 🔢 Числа и операторы

```python
# Арифметика
2 + 3    # 5       (сложение)
5 - 2    # 3       (вычитание)
3 * 4    # 12      (умножение)
10 / 3   # 3.333.. (деление, всегда float)
10 // 3  # 3       (целочисленное)
10 % 3   # 1       (остаток)
2 ** 3   # 8       (степень)

# Сравнения → True/False
x == y   # равно
x != y   # не равно
x > y    # больше
x >= y   # больше или равно
x < y    # меньше
x <= y   # меньше или равно
x is None  # проверка на None

# Логические
a and b   # И (оба True)
a or b    # ИЛИ (хотя бы один True)
not a     # НЕ

# Принадлежность
"a" in "abc"       # True
5 in [1, 2, 3]     # False
"key" in {"key": 1} # True (ключи)
```

---

## 🔤 Строки

```python
s = "Hello, World!"

# Базовые методы
len(s)           # 13
s.upper()        # "HELLO, WORLD!"
s.lower()        # "hello, world!"
s.title()        # "Hello, World!"
s.strip()        # Убрать пробелы по краям
s.replace("H", "J")  # "Jello, World!"
s.split(", ")    # ["Hello", "World!"]
", ".join(["a", "b"])  # "a, b"
s.find("World")  # 7 (индекс или -1)
"World" in s     # True

# Срезы [начало:конец:шаг]
s[0]     # 'H'
s[-1]    # '!'
s[0:5]   # 'Hello'
s[7:]    # 'World!'
s[::2]   # 'Hlo ol!'
s[::-1]  # '!dlroW ,olleH' (переворот)

# Проверки
s.startswith("He")  # True
s.endswith("!")     # True
s.isdigit()         # False (только цифры?)
"123".isdigit()     # True
```

---

## 📋 Списки

```python
fruits = ["яблоко", "банан", "киви"]

# Доступ
fruits[0]          # "яблоко"
fruits[-1]         # "киви"
fruits[1:3]        # ["банан", "киви"]
len(fruits)        # 3

# Изменение
fruits.append("манго")     # Добавить в конец
fruits.insert(1, "груша")  # Вставить по индексу
fruits.remove("банан")     # Удалить по значению
fruits.pop()               # Удалить последний (возвращает)
fruits.pop(0)              # Удалить по индексу
fruits.sort()              # Сортировка на месте
sorted(fruits)             # Новая отсортированная копия
fruits.reverse()           # Переворот на месте
"яблоко" in fruits         # True

# Копирование
copy = fruits.copy()       # Поверхностная копия
copy = fruits[:]           # То же самое
copy = list(fruits)        # И так тоже

# List comprehension
[x**2 for x in range(5)]           # [0, 1, 4, 9, 16]
[x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

---

## 📖 Словари

```python
user = {"name": "Анна", "age": 28, "city": "Москва"}

# Доступ
user["name"]           # "Анна"
user.get("name")        # "Анна" (безопасно)
user.get("email", "—")  # "—" (значение по умолчанию)
len(user)               # 3 (количество пар)

# Изменение
user["email"] = "a@mail.com"  # Добавить/обновить
user.update({"age": 29})      # Обновить несколько
user.pop("city")              # Удалить и вернуть
user.popitem()                # Удалить последнюю пару
del user["age"]               # Удалить по ключу

# Итерация
for key in user:              # По ключам
for key, value in user.items():  # По парам
for value in user.values():   # По значениям

# Проверки
"name" in user          # True
"name" in user.keys()   # True (то же самое)

# Dict comprehension
{x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

---

## 🔀 Условия

```python
if age >= 18:
    print("Можно")
elif age >= 16:
    print("С родителями")
else:
    print("Нельзя")

# Тернарный оператор
status = "Взрослый" if age >= 18 else "Ребёнок"

# match/case (Python 3.10+)
match command:
    case "start": start()
    case "stop":  stop()
    case _:       print("Неизвестно")  # default
```

---

## 🔁 Циклы

```python
# for
for i in range(5):         # 0, 1, 2, 3, 4
for item in my_list:       # По элементам
for key, val in dict.items():  # По словарю
for i, item in enumerate(lst): # С индексом
for a, b in zip(list1, list2): # Параллельно

# while
while count < 10:
    count += 1
while True:          # Бесконечный
    if done: break

# Управление
break      # Выйти из цикла
continue   # Следующая итерация
```

---

## 🔧 Функции

```python
def add(a: int, b: int = 0) -> int:
    """Складывает два числа."""
    return a + b

# *args и **kwargs
def func(*args, **kwargs):
    print(args)    # Кортеж позиционных
    print(kwargs)  # Словарь именованных

# lambda (анонимная)
square = lambda x: x ** 2
sorted(users, key=lambda u: u["age"])
```

---

## 📁 Файлы

```python
# Чтение
with open("file.txt", "r", encoding="utf-8") as f:
    text = f.read()          # Весь файл
    lines = f.readlines()    # Список строк
    for line in f:           # Построчно (экономит память!)

# Запись
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("Текст\n")

# pathlib (современный способ)
from pathlib import Path
path = Path("dir/file.txt")
path.exists()          # Существует?
path.read_text()       # Прочитать
path.write_text("txt") # Записать
path.parent            # Родительская директория
path.name              # Имя файла
```

---

## 🌐 JSON

```python
import json

# Чтение
with open("data.json") as f:
    data = json.load(f)        # Из файла
data = json.loads('{"key": "value"}')  # Из строки

# Запись
json.dumps(obj, ensure_ascii=False, indent=2)  # В строку
json.dump(obj, f, ensure_ascii=False, indent=2)  # В файл
```

---

## ⚠️ Исключения

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("На ноль делить нельзя!")
except (ValueError, TypeError) as e:
    print(f"Ошибка: {e}")
else:
    print(f"Успех: {result}")
finally:
    print("Выполнится всегда")
```

---

## 🧪 Тестирование (pytest)

```python
# test_math.py
import pytest

def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

@pytest.mark.parametrize("a,b,expected", [(1,2,3), (0,0,0)])
def test_param(a, b, expected):
    assert add(a, b) == expected
```

---

## 📅 Даты

```python
from datetime import datetime, date, timedelta

now = datetime.now()
today = date.today()
specific = datetime(2024, 6, 15, 14, 30)

# Форматирование
now.strftime("%d.%m.%Y %H:%M")  # "15.06.2024 14:30"
datetime.strptime("15.06.2024", "%d.%m.%Y")

# Арифметика
tomorrow = today + timedelta(days=1)
diff = date(2025, 1, 1) - today
```

---

## 🗄️ SQLite

```python
import sqlite3

conn = sqlite3.connect("db.sqlite")
conn.row_factory = sqlite3.Row  # Доступ по именам

# SELECT
for row in conn.execute("SELECT * FROM users WHERE age > ?", (18,)):
    print(row["name"])

# INSERT/UPDATE/DELETE
conn.execute("INSERT INTO users (name) VALUES (?)", ("Анна",))
conn.execute("UPDATE users SET name = ? WHERE id = ?", ("Новое", 1))
conn.execute("DELETE FROM users WHERE id = ?", (5,))
conn.commit()
```

---

## ⚡ Полезные встроенные функции

```python
len(seq)            # Длина
type(obj)           # Тип
range(start, stop, step)  # Последовательность чисел
enumerate(seq)      # (индекс, элемент)
zip(seq1, seq2)     # Параллельная итерация
map(func, seq)      # Применить функцию к каждому
filter(func, seq)   # Оставить по условию
sorted(seq, key=func)  # Отсортировать
reversed(seq)       # Перевернуть
any(seq)            # Хотя бы один True
all(seq)            # Все True
sum(seq)            # Сумма
min(seq), max(seq)  # Минимум, максимум
abs(x)              # Модуль
round(x, n)         # Округление
```

---

## 🎯 Типизация (type hints)

```python
def greet(name: str, age: int) -> str:
    return f"{name}, {age} лет"

names: list[str] = ["Анна", "Борис"]
data: dict[str, int] = {"a": 1}
maybe: str | None = None      # Python 3.10+
```

---

## 📊 Comprehensions

```python
# List
[x**2 for x in range(5) if x % 2 == 0]

# Dict
{x: x**2 for x in range(5)}

# Set
{x**2 for x in range(-3, 4)}

# Generator (ленивый!)
(x**2 for x in range(10**6))
```

---

## 🔍 Regex

```python
import re

re.search(r"\d+", text)          # Первое число
re.findall(r"\d+", text)         # Все числа
re.sub(r"\d", "X", text)         # Замена цифр на X
re.split(r"[,.]", text)          # Разделить по , или .
```
