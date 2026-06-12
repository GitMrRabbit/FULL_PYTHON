"""
Ответы к упражнениям уроков 10-19 (Функции, ООП, Декораторы)
=============================================================

Сначала решите САМИ, потом сверяйтесь!
"""

# =============================================================================
# Урок 10: Функции
# =============================================================================

# Упражнение 1: Палиндром
def is_palindrome(s: str) -> bool:
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]

# Упражнение 2: Бинарный поиск
def binary_search(sorted_list: list, target) -> int:
    left, right = 0, len(sorted_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Упражнение 3: Декоратор @retry(n)
import functools
import time

def retry(max_attempts):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(0.5)
        return wrapper
    return decorator

# Упражнение 4: Генератор chunks
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# =============================================================================
# Урок 15: ООП Основы
# =============================================================================

class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def __repr__(self):
        return f"Rectangle({self.width}, {self.height})"


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0")
        self._balance += amount

    def withdraw(self, amount: float) -> bool:
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def transfer(self, amount: float, other: "BankAccount") -> bool:
        if self.withdraw(amount):
            other.deposit(amount)
            return True
        return False

    @property
    def balance(self) -> float:
        return self._balance


from dataclasses import dataclass, field

@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int = 1

@dataclass
class Order:
    id: int
    items: list[OrderItem] = field(default_factory=list)
    status: str = "new"

    def total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)

    def add_item(self, item: OrderItem):
        self.items.append(item)


import math

class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"


# =============================================================================
# Урок 16: Наследование
# =============================================================================

class Vehicle:
    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model

    def move(self) -> str:
        return "Транспорт движется"

class Car(Vehicle):
    def move(self) -> str:
        return f"{self.brand} {self.model} едет по дороге"

class Motorcycle(Vehicle):
    def move(self) -> str:
        return f"{self.brand} {self.model} мчит по трассе"

class Bicycle(Vehicle):
    def move(self) -> str:
        return f"{self.brand} {self.model} катится по тропинке"


from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message: str, level: str = "INFO") -> None:
        ...

class FileLogger(Logger):
    def __init__(self, path: str):
        self.path = path

    def log(self, message: str, level: str = "INFO") -> None:
        with open(self.path, "a") as f:
            f.write(f"[{level}] {message}\n")

class ConsoleLogger(Logger):
    def log(self, message: str, level: str = "INFO") -> None:
        print(f"[{level}] {message}")


# =============================================================================
# Урок 17: Магические методы
# =============================================================================

class Matrix:
    def __init__(self, data: list[list[float]]):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __add__(self, other):
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __mul__(self, other):
        if isinstance(other, Matrix):
            result = [[0] * other.cols for _ in range(self.rows)]
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        result[i][j] += self.data[i][k] * other.data[k][j]
            return Matrix(result)
        return Matrix([[x * other for x in row] for row in self.data])

    def __getitem__(self, idx):
        return self.data[idx]

    def __repr__(self):
        return "\n".join(str(row) for row in self.data)


class MyRange:
    def __init__(self, *args):
        if len(args) == 1:
            self.start, self.stop, self.step = 0, args[0], 1
        elif len(args) == 2:
            self.start, self.stop, self.step = args[0], args[1], 1
        else:
            self.start, self.stop, self.step = args

    def __iter__(self):
        current = self.start
        while (self.step > 0 and current < self.stop) or \
              (self.step < 0 and current > self.stop):
            yield current
            current += self.step

    def __len__(self):
        if self.step > 0 and self.start >= self.stop:
            return 0
        if self.step < 0 and self.start <= self.stop:
            return 0
        return max(0, (self.stop - self.start + self.step - (1 if self.step > 0 else -1)) // self.step)

    def __contains__(self, item):
        if self.step > 0:
            return self.start <= item < self.stop and (item - self.start) % self.step == 0
        return self.stop < item <= self.start and (item - self.start) % self.step == 0


class TempDir:
    import tempfile, shutil
    def __enter__(self):
        self.path = self.tempfile.mkdtemp()
        return self.path
    def __exit__(self, *args):
        self.shutil.rmtree(self.path)


class Money:
    def __init__(self, amount: float, currency: str = "RUB"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Разные валюты!")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Разные валюты!")
        return Money(self.amount - other.amount, self.currency)

    def __repr__(self):
        return f"{self.amount:.2f} {self.currency}"


# =============================================================================
# Урок 18: Properties
# =============================================================================

class Temperature:
    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9

    @property
    def kelvin(self):
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value):
        self._celsius = value - 273.15


import json

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @classmethod
    def from_json(cls, json_str: str) -> "User":
        data = json.loads(json_str)
        return cls(data["name"], data["email"])

    @staticmethod
    def is_valid_email(email: str) -> bool:
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))


# =============================================================================
# Урок 19: Декораторы
# =============================================================================

import signal

def timeout(seconds: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import multiprocessing
            def target(queue, *a, **kw):
                queue.put(func(*a, **kw))
            queue = multiprocessing.Queue()
            process = multiprocessing.Process(target=target, args=(queue, *args), kwargs=kwargs)
            process.start()
            process.join(seconds)
            if process.is_alive():
                process.terminate()
                raise TimeoutError(f"Функция не завершилась за {seconds}с")
            return queue.get()
        return wrapper
    return decorator


def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


def log_to_file(filename: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "a") as f:
                f.write(f"{func.__name__}({args}, {kwargs}) → {result}\n")
            return result
        return wrapper
    return decorator


# =============================================================================
# САМОПРОВЕРКА
# =============================================================================

if __name__ == "__main__":
    print("Проверка ответов к урокам 10-19:\n")

    # Урок 10
    assert is_palindrome("А роза упала на лапу Азора") == True
    assert binary_search([1, 3, 5, 7, 9], 5) == 2
    assert binary_search([1, 3, 5, 7, 9], 4) == -1
    print("✓ Урок 10 (Функции)")

    # Урок 15
    r = Rectangle(4, 5)
    assert r.area() == 20.0
    assert r.perimeter() == 18.0
    print("✓ Урок 15 (ООП Основы)")

    # Урок 16
    car = Car("Toyota", "Camry")
    assert "едет" in car.move()
    print("✓ Урок 16 (Наследование)")

    # Урок 18
    t = Temperature(0)
    assert t.fahrenheit == 32.0
    t.fahrenheit = 212
    assert t.celsius == 100.0
    print("✓ Урок 18 (Properties)")

    print("\n✅ Все проверки пройдены!")
