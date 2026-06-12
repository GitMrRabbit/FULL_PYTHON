# 🔁 Урок 06: Циклы в Python

## 📖 Теория

Циклы позволяют многократно выполнять блок кода. Python поддерживает два типа циклов: `for` и `while`.

---

## 🔹 Цикл `for`

Используется для итерации по последовательностям (списки, строки, словари, range и т.д.):

```python
# Итерация по списку
for item in [1, 2, 3, 4, 5]:
    print(item)

# Итерация по строке
for char in "Python":
    print(char)

# Итерация по словарю
d = {"a": 1, "b": 2}
for key in d:                  # По ключам (по умолчанию)
    print(key)
for value in d.values():       # По значениям
    print(value)
for key, value in d.items():   # По парам ключ-значение
    print(f"{key} -> {value}")
```

---

## 🔹 `range()` — генератор числовых последовательностей

```python
range(stop)              # 0, 1, 2, ..., stop-1
range(start, stop)       # start, start+1, ..., stop-1
range(start, stop, step) # С шагом step (может быть отрицательным!)

list(range(5))         # [0, 1, 2, 3, 4]
list(range(2, 7))      # [2, 3, 4, 5, 6]
list(range(0, 10, 2))  # [0, 2, 4, 6, 8]  — чётные
list(range(10, 0, -1)) # [10, 9, 8, ..., 1] — обратный отсчёт
```

---

## 🔹 `enumerate()` — итерация с индексом

```python
fruits = ["яблоко", "банан", "вишня"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: яблоко, 1: банан, 2: вишня

for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
# 1. яблоко, 2. банан, 3. вишня
```

---

## 🔹 `zip()` — параллельная итерация

```python
names = ["Анна", "Борис", "Вера"]
ages  = [28, 35, 22]

for name, age in zip(names, ages):
    print(f"{name}: {age} лет")

# Разная длина — до самой короткой
for a, b in zip([1, 2, 3], "ab"):  # Только 2 итерации
    print(a, b)

# zip_longest — до самой длинной
from itertools import zip_longest
for a, b in zip_longest([1, 2, 3], "ab", fillvalue=None):
    print(a, b)  # (3, None)
```

---

## 🔹 Цикл `while`

Выполняется, пока условие истинно:

```python
count = 0
while count < 5:
    print(count)
    count += 1

# Бесконечный цикл с выходом
while True:
    user_input = input("Введите 'exit': ")
    if user_input == "exit":
        break
```

---

## 🚦 Управление циклом

| Ключевое слово | Действие |
|---------------|----------|
| `break` | Немедленный выход из цикла |
| `continue` | Переход к следующей итерации |
| `pass` | Пустой блок (ничего не делает) |
| `else` (после цикла) | Выполняется, если цикл завершился **без** `break` |

```python
# break — выход из цикла
for i in range(10):
    if i == 5:
        break           # Цикл прервётся на i=5
    print(i)            # 0 1 2 3 4

# continue — пропуск итерации
for i in range(5):
    if i == 2:
        continue        # Пропускаем 2
    print(i)            # 0 1 3 4

# else после цикла
for i in range(5):
    if i == 10:         # Никогда не сработает
        break
else:
    print("Цикл завершился без break!")  # Выполнится

for i in range(5):
    if i == 3:
        break
else:
    print("Это не выполнится")  # Не выполнится (был break)
```

---

## 🧩 List Comprehensions (генераторы списков)

Компактный способ создавать списки в одну строку:

```python
# Обычный цикл
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension
squares = [x ** 2 for x in range(10)]

# С условием
evens = [x for x in range(20) if x % 2 == 0]

# С if/else
labels = ["чёт" if x % 2 == 0 else "нечет" for x in range(5)]

# Вложенные циклы
pairs = [(x, y) for x in range(3) for y in range(3)]
```

---

## ⚡ Производительность

```python
# Медленно (много вызовов append)
result = []
for i in range(10000):
    result.append(i * 2)

# Быстрее (list comprehension)
result = [i * 2 for i in range(10000)]

# Ещё быстрее (map + list)
result = list(map(lambda x: x * 2, range(10000)))
```

---

## ⚠️ Частые ошибки

```python
# ❌ Изменение списка во время итерации
for item in my_list:
    if should_remove(item):
        my_list.remove(item)  # Пропускает элементы!

# ✅ Правильно: итерация по копии
for item in my_list[:]:       # Или list(my_list)
    if should_remove(item):
        my_list.remove(item)

# ✅ Или: построение нового списка
my_list = [item for item in my_list if not should_remove(item)]

# ❌ Бесконечный while
while True:
    pass  # Ctrl+C!

# ✅ Всегда предусматривайте условие выхода
```

---

## 💡 Лучшие практики

1. **`for` предпочтительнее `while`** — когда знаете количество итераций
2. **`enumerate()` вместо `range(len())`** — более читаемо
3. **List comprehension для простых преобразований** — быстрее и короче
4. **Избегайте `else` после циклов** — неочевидное поведение для новичков
5. **`break` и `continue` используйте умеренно** — может усложнить чтение

---

## 🧪 Упражнения

1. Выведите таблицу умножения (9x9) используя вложенные циклы
2. Напишите функцию `find_primes(n)` — найти все простые числа до n
3. Реализуйте FizzBuzz от 1 до 100
4. Используя list comprehension, создайте список всех букв строки в верхнем регистре, кроме гласных
5. Реализуйте игру «угадай число» с циклом `while`
