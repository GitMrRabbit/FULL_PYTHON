# ✨ Урок 17: Магические методы (Dunder Methods)

## 📖 Теория

Магические методы (dunder = double underscore) — методы вида `__имя__`, которые Python вызывает автоматически. Они позволяют настраивать поведение объектов.

---

## 📋 Категории магических методов

| Категория | Методы | Когда вызываются |
|-----------|--------|-----------------|
| Создание | `__init__`, `__new__`, `__del__` | Создание/удаление объекта |
| Строки | `__str__`, `__repr__`, `__format__` | `str()`, `repr()`, f-строки |
| Коллекции | `__len__`, `__getitem__`, `__setitem__` | `len()`, `obj[i]` |
| Итерация | `__iter__`, `__next__` | `for x in obj` |
| Вызов | `__call__` | `obj()` |
| Контекст | `__enter__`, `__exit__` | `with obj:` |
| Сравнение | `__eq__`, `__lt__`, `__gt__`, `__hash__` | `==`, `<`, `>`, `hash()` |
| Арифметика | `__add__`, `__sub__`, `__mul__` | `+`, `-`, `*` |
| Атрибуты | `__getattr__`, `__setattr__` | `obj.attr` |
| Преобразование | `__bool__`, `__int__`, `__float__` | `bool()`, `int()` |

---

## 🔹 Эмуляция коллекций

```python
class MyList:
    def __getitem__(self, index):
        return self._data[index]     # obj[0]

    def __setitem__(self, index, value):
        self._data[index] = value    # obj[0] = x

    def __len__(self):
        return len(self._data)       # len(obj)

    def __contains__(self, item):
        return item in self._data    # x in obj
```

---

## 🔹 Итераторы

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self                  # Итератор — сам себе

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

for n in Countdown(3):  # 3, 2, 1, 0
    print(n)
```

---

## 🔹 Контекстные менеджеры

```python
class ManagedFile:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.file = open(self.path, 'r')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        # return True → подавить исключение
        # return False → пробросить (по умолчанию)

with ManagedFile("data.txt") as f:
    content = f.read()
```

---

## 🔹 Вызываемые объекты

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
double(5)  # 10 — объект вызывается как функция!
```

---

## 🔹 Арифметические операции

```python
class Vector:
    def __add__(self, other):    # self + other
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):   # self * scalar
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):  # scalar * self
        return self.__mul__(scalar)

    def __neg__(self):           # -self
        return Vector(-self.x, -self.y)

    def __abs__(self):           # abs(self)
        return (self.x**2 + self.y**2) ** 0.5
```

---

## 🧪 Упражнения

1. Реализуйте класс `Matrix` с `__add__`, `__mul__`, `__getitem__`
2. Создайте класс `Range` с поддержкой `__iter__`, `__len__`, `__contains__`
3. Напишите контекстный менеджер `TempDir`, создающий и автоматически удаляющий временную директорию
4. Реализуйте класс `Money` с поддержкой арифметических операций и форматирования в разных валютах
