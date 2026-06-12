# 📋 Урок 07: Списки (Lists) в Python

## 📖 Теория

Список (`list`) — упорядоченная, изменяемая коллекция элементов. Самый часто используемый тип данных в Python.

---

## 🔹 Создание списков

```python
# Пустой список
empty = []
empty = list()

# С элементами
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None, [1, 2]]  # Можно смешивать типы

# Из других коллекций
chars = list("hello")       # ['h', 'e', 'l', 'l', 'o']
from_range = list(range(5)) # [0, 1, 2, 3, 4]
```

---

## 🔹 Доступ по индексу и срезы

```python
lst = [10, 20, 30, 40, 50]

# Индексация
lst[0]    # 10    — первый
lst[-1]   # 50    — последний
lst[2]    # 30

# Срезы [start:stop:step]
lst[1:4]   # [20, 30, 40]
lst[:3]    # [10, 20, 30]  — от начала до 3
lst[2:]    # [30, 40, 50]  — с 2 до конца
lst[::2]   # [10, 30, 50]  — каждый второй
lst[::-1]  # [50, 40, 30, 20, 10] — реверс!
```

---

## 🔹 Основные методы списков

### Добавление элементов
```python
lst.append(x)       # Добавить в конец
lst.insert(i, x)    # Вставить на позицию i
lst.extend(iter)    # Добавить все элементы из iterable
```

### Удаление элементов
```python
lst.remove(x)       # Удалить первое вхождение x (ошибка, если нет)
lst.pop(i)          # Удалить и вернуть элемент по индексу (по умолчанию последний)
lst.clear()         # Очистить список
del lst[i]          # Удалить по индексу (не метод, а оператор)
del lst[1:3]        # Удалить срез
```

### Поиск и подсчёт
```python
lst.index(x)        # Индекс первого вхождения x
lst.count(x)        # Количество вхождений x
x in lst            # Проверка наличия (True/False)
```

### Сортировка
```python
lst.sort()                    # На месте (изменяет список)
lst.sort(reverse=True)        # По убыванию
lst.sort(key=len)             # По длине элементов
sorted(lst)                   # Возвращает новый отсортированный список (не меняет исходный)
```

### Другие
```python
lst.reverse()       # Перевернуть на месте
lst.copy()          # Поверхностная копия
len(lst)            # Длина списка
```

---

## 🔹 Копирование списков

```python
# ❌ Это НЕ копия, а ссылка на тот же объект!
a = [1, 2, 3]
b = a               # b и a указывают на один и тот же список!
b.append(4)
print(a)            # [1, 2, 3, 4] — a тоже изменился!

# ✅ Поверхностная копия (shallow copy)
b = a.copy()
b = a[:]
b = list(a)

# Глубокая копия (deep copy) — для вложенных структур
import copy
b = copy.deepcopy(a)
```

---

## 🔹 Стек и очередь

```python
# Стек (LIFO — Last In, First Out)
stack = []
stack.append(1)     # push
stack.append(2)
stack.append(3)
stack.pop()         # 3
stack.pop()         # 2

# Очередь (FIFO — First In, First Out)
from collections import deque
queue = deque()
queue.append(1)
queue.append(2)
queue.popleft()     # 1
queue.popleft()     # 2
```

---

## 🔹 List Comprehensions

```python
# Базовый синтаксис
[x**2 for x in range(5)]           # [0, 1, 4, 9, 16]

# С условием
[x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# С if/else
["чёт" if x % 2 == 0 else "нечет" for x in range(5)]

# Вложенные
[(x, y) for x in range(3) for y in range(2)]

# Из словаря
[v * 2 for k, v in {"a": 1, "b": 2}.items()]
```

---

## ⚠️ Частые ошибки

```python
# ❌ IndexError — выход за границы
lst = [1, 2, 3]
lst[10]  # IndexError!

# ❌ Изменение списка во время итерации
for item in lst:
    if item == 2:
        lst.remove(item)  # Пропускает элементы!

# ✅ Итерация по копии
for item in lst[:]:
    if item == 2:
        lst.remove(item)

# ❌ Умножение вложенных списков
grid = [[0] * 3] * 3  # Все строки — один и тот же список!
grid[0][0] = 1
print(grid)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] — неожиданно!

# ✅ Правильно
grid = [[0] * 3 for _ in range(3)]
```

---

## 🧪 Упражнения

1. Реализуйте функцию `remove_duplicates(lst)`, сохраняющую порядок
2. Напишите функцию `flatten(nested_list)` для «сплющивания» вложенных списков
3. Реализуйте транспонирование матрицы (двумерного списка)
4. Найдите пересечение двух списков без использования множеств
