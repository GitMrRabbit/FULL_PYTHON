# 🏗️ Урок 15: ООП — Основы (Классы и Объекты)

## 📖 Теория

**ООП (Объектно-Ориентированное Программирование)** — парадигма, основанная на концепции объектов, содержащих данные (атрибуты) и поведение (методы).

---

## 🔹 Класс vs Объект

- **Класс** — шаблон/чертёж (например, `Person`)
- **Объект (экземпляр)** — конкретная реализация (например, `alice = Person("Алиса", 28)`)

```python
class Person:
    species = "Homo Sapiens"    # Атрибут класса (общий для всех)

    def __init__(self, name, age):
        self.name = name         # Атрибут экземпляра
        self.age = age

    def greet(self):             # Метод экземпляра
        return f"Привет, я {self.name}"
```

---

## 🔹 `self` — ссылка на экземпляр

- `self` — первый параметр каждого метода экземпляра
- При вызове `alice.greet()` Python передаёт `alice` как `self`
- Имя `self` — соглашение (можно любое, но НЕ МЕНЯЙТЕ!)

---

## 🔹 `__init__` — конструктор

```python
class Person:
    def __init__(self, name: str, age: int = 0):
        self.name = name
        self.age = age
        print(f"Создан: {self}")

alice = Person("Алиса", 28)  # __init__ вызывается автоматически
```

---

## 🔹 `__str__` и `__repr__`

```python
class Point:
    def __str__(self):   # Для пользователей: print(obj), str(obj)
        return f"Point({self.x}, {self.y})"

    def __repr__(self):  # Для разработчиков: repr(obj), в консоли
        return f"Point(x={self.x!r}, y={self.y!r})"
```

| Функция | `__str__` | `__repr__` |
|---------|-----------|-----------|
| Цель | Читаемое представление | Однозначное, для отладки |
| Вызывается | `print()`, `str()`, f-строки | `repr()`, консоль, список |
| Если нет `__str__` | — | Используется `__repr__` |

---

## 🔹 Инкапсуляция

В Python нет настоящих private-полей, только соглашения:

```python
class Example:
    def __init__(self):
        self.public = 1         # Доступен всем
        self._protected = 2     # Соглашение: "внутренний" (не трогать снаружи)
        self.__private = 3      # Name mangling → _Example__private
```

**Name mangling**: `__attr` → `_ClassName__attr` (не для безопасности, а для предотвращения конфликтов при наследовании).

---

## 🔹 `@dataclass` (Python 3.7+)

Автоматически генерирует `__init__`, `__repr__`, `__eq__`:

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True
    tags: list[str] = field(default_factory=list)  # default_factory для изменяемых!

@dataclass(frozen=True)  # Неизменяемый
class Point:
    x: float
    y: float
```

---

## 💡 4 принципа ООП

| Принцип | Описание |
|----------|----------|
| **Инкапсуляция** | Сокрытие внутренней реализации |
| **Наследование** | Создание новых классов на основе существующих |
| **Полиморфизм** | Один интерфейс — разные реализации |
| **Абстракция** | Выделение существенных характеристик |

---

## 🧪 Упражнения

1. Создайте класс `Rectangle` с методами `area()` и `perimeter()`
2. Реализуйте класс `BankAccount` с методами `deposit()`, `withdraw()`, `transfer()`
3. Используя `@dataclass`, создайте модель `Order` с товарами и статусом
4. Создайте класс `Vector2D` с переопределёнными `__add__`, `__sub__`, `__eq__`
