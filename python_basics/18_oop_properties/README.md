# 🔐 Урок 18: ООП — Свойства, @classmethod, @staticmethod

## 📖 Теория

Углублённое ООП: управление доступом к атрибутам через `@property`, методы класса и статические методы.

---

## 🔹 `@property` — вычисляемые атрибуты

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):           # Геттер: circle.radius (без скобок!)
        return self._radius

    @radius.setter
    def radius(self, value):    # Сеттер: circle.radius = 5
        if value < 0:
            raise ValueError("Радиус >= 0!")
        self._radius = value

    @radius.deleter
    def radius(self):           # Делетер: del circle.radius
        self._radius = 0

    @property
    def area(self):             # Только для чтения (нет сеттера)
        return 3.14159 * self._radius ** 2
```

**Зачем?**
- Валидация при присваивании
- Вычисляемые значения (как атрибуты, а не методы)
- Обратная совместимость (можно заменить атрибут на property без изменения API)
- Инкапсуляция (скрываем `_radius`, предоставляем `radius`)

---

## 🔹 `@classmethod` — методы класса

```python
class Person:
    population = 0

    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year
        Person.population += 1

    @classmethod
    def from_birth_date(cls, name, date_str):
        """Альтернативный конструктор."""
        year = int(date_str.split("-")[0])
        return cls(name, year)  # cls = Person

    @classmethod
    def get_population(cls):
        return cls.population

# Использование
p = Person.from_birth_date("Анна", "1995-05-15")
print(Person.get_population())
```

Первый параметр — `cls` (сам класс, не экземпляр).

---

## 🔹 `@staticmethod` — статические методы

```python
class MathUtils:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))

# Без создания экземпляра
MathUtils.is_even(4)   # True
MathUtils.clamp(15, 0, 10)  # 10
```

Ни `self`, ни `cls`. Просто функция, логически связанная с классом.

---

## 🔹 `__slots__` — оптимизация памяти

```python
class Point:
    __slots__ = ("x", "y")   # Фиксированный набор атрибутов
    def __init__(self, x, y):
        self.x = x
        self.y = y

# НЕТ __dict__! Экономия памяти (~50%).
# НЕЛЬЗЯ добавить новые атрибуты: p.z = 3  # AttributeError!
```

Используйте для миллионов мелких объектов (точки, узлы графа, записи логов).

---

## 📊 Сравнение методов

| Тип метода | 1-й параметр | Доступ к | Использование |
|-----------|-------------|---------|--------------|
| Обычный | `self` | Экземпляр + класс | `obj.method()` |
| `@classmethod` | `cls` | Класс (не экземпляр) | `Class.method()`, фабрики |
| `@staticmethod` | — | Ничего автоматически | `Class.method()`, утилиты |
| `@property` | `self` | Как атрибут | `obj.prop` (без скобок) |

---

## 🧪 Упражнения

1. Создайте класс `Temperature` с конвертацией °C ↔ °F ↔ K через `@property`
2. Реализуйте `@classmethod` для создания объекта из JSON-строки
3. Добавьте `@staticmethod` для валидации email в классе `User`
4. Используйте `__slots__` для оптимизации класса `LogEntry` (timestamp, level, message)
