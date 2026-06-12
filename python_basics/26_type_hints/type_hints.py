"""
Урок 26: Type Hints (Аннотации типов) в Python
================================================

Темы:
  - Базовые типы: int, float, str, bool, None
  - Коллекции: list[int], dict[str, int], tuple[str, float], set[int]
  - Union, Optional, Any
  - Callable, TypeAlias, NewType
  - TypedDict, NamedTuple
  - Protocol (структурная типизация)
  - @dataclass (уже знакомы)
  - TypeVar, Generic
  - mypy / pyright — статическая проверка типов
"""

from typing import (
    Any, Union, Optional, Callable, TypeVar, Generic,
    TypedDict, NamedTuple, Protocol, NewType, TypeAlias,
    Literal, Final, ClassVar
)
from dataclasses import dataclass
from collections.abc import Sequence, Iterable, Mapping


# =============================================================================
# 1. БАЗОВЫЕ ТИПЫ
# =============================================================================

def greet(name: str, age: int) -> str:
    """
    Простая функция с type hints.
    name: str — ожидаем строку
    age: int — ожидаем целое
    -> str — возвращаем строку
    """
    return f"{name}, {age} лет"


def process_data(data: list[int], config: dict[str, Any] | None = None) -> bool:
    """
    data: список целых чисел (Python 3.9+: list[int])
    config: словарь или None (Python 3.10+: X | None вместо Optional[X])
    -> bool: возвращает True/False
    """
    if config is None:
        config = {}
    return len(data) > 0


def basic_types_demo():
    """Демонстрация базовых type hints."""
    print("=" * 60)
    print("1. БАЗОВЫЕ ТИПЫ")
    print("=" * 60)

    # Простые типы
    name: str = "Анна"
    age: int = 28
    height: float = 1.75
    is_student: bool = False
    nothing: None = None

    # Коллекции (Python 3.9+)
    scores: list[int] = [95, 88, 92]
    user: dict[str, Any] = {"name": "Анна", "age": 28}
    point: tuple[float, float] = (3.0, 4.0)
    tags: set[str] = {"python", "testing"}

    # Union / Optional
    result: str | None = None  # Python 3.10+
    value: Optional[int] = None  # Эквивалентно int | None

    # Any — любой тип (нет проверки)
    dynamic: Any = "может быть чем угодно"
    dynamic = 42  # mypy не ругается

    print(f"greet('Анна', 28) = {greet('Анна', 28)}")
    print(f"process_data([1,2,3]) = {process_data([1, 2, 3])}")

    # Type hints НЕ проверяются во время выполнения!
    # Для проверки нужен mypy или pyright
    result_bad = greet("Анна", "двадцать восемь")  # Нет ошибки во время выполнения!
    print(f"greet с неправильным типом: {result_bad}")
    print("  (type hints не проверяются во время выполнения — нужен mypy)")


# =============================================================================
# 2. CALLABLE, TYPEALIAS, NEWTYPE
# =============================================================================

# TypeAlias — псевдоним типа (Python 3.10+)
UserId: TypeAlias = int
JsonDict: TypeAlias = dict[str, Any]

# NewType — отдельный тип (строгая проверка mypy)
UserID = NewType("UserID", int)
ProductID = NewType("ProductID", int)

# Callable — функция
Comparator = Callable[[int, int], bool]  # (аргументы) → возврат


def get_user(user_id: UserId) -> JsonDict:
    """Принимает UserID, возвращает JsonDict."""
    return {"id": user_id, "name": "User"}


def sort_items(items: list[int], cmp: Callable[[int, int], bool]) -> list[int]:
    return sorted(items, key=functools.cmp_to_key(cmp))


import functools


def type_aliases_demo():
    """Демонстрация TypeAlias, NewType, Callable."""
    print("\n" + "=" * 60)
    print("2. TYPEALIAS, NEWTYPE, CALLABLE")
    print("=" * 60)

    uid = UserID(42)
    pid = ProductID(42)

    # mypy поймает: UserID != ProductID
    # get_user(pid)  # Ошибка mypy!

    user = get_user(uid)
    print(f"get_user({uid}) = {user}")

    # Callable
    def descending(a: int, b: int) -> bool:
        return a > b

    result = sort_items([3, 1, 4, 1, 5], descending)
    print(f"sort_items descending: {result}")


# =============================================================================
# 3. TYPEDDICT, NAMEDTUPLE, PROTOCOL
# =============================================================================

class UserDict(TypedDict):
    """TypedDict — словарь с известной структурой."""
    name: str
    age: int
    email: str


class PointNT(NamedTuple):
    """NamedTuple с type hints."""
    x: float
    y: float
    label: str = ""


class Drawable(Protocol):
    """Protocol — структурная типизация (не нужно наследовать!)."""

    def draw(self) -> str:
        ...

    def area(self) -> float:
        ...


class Circle:
    """Реализует Drawable НЕ наследуя от него! (структурная типизация)"""

    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"○({self.radius})"

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2


class Rectangle:
    def draw(self) -> str:
        return "▯"

    def area(self) -> float:
        return 100.0


def render(shape: Drawable) -> str:
    """Принимает любой объект с .draw() и .area() — утиная типизация!"""
    return f"{shape.draw()} (площадь: {shape.area():.2f})"


def typeddict_protocol_demo():
    """Демонстрация TypedDict, Protocol."""
    print("\n" + "=" * 60)
    print("3. TYPEDDICT, PROTOCOL")
    print("=" * 60)

    # TypedDict
    user: UserDict = {"name": "Анна", "age": 28, "email": "anna@example.com"}
    print(f"UserDict: {user}")

    # NamedTuple
    p = PointNT(3.0, 4.0, "origin")
    print(f"PointNT: {p}, x={p.x}, y={p.y}")

    # Protocol
    shapes: list[Drawable] = [Circle(5), Rectangle()]
    for shape in shapes:
        print(f"  render({shape.__class__.__name__}): {render(shape)}")


# =============================================================================
# 4. TYPEVAR, GENERIC
# =============================================================================

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class Stack(Generic[T]):
    """Обобщённый (generic) стек."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T | None:
        return self._items.pop() if self._items else None

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)


def first(items: Sequence[T]) -> T | None:
    """Обобщённая функция: возвращает первый элемент."""
    return items[0] if items else None


def generic_demo():
    """Демонстрация обобщённых типов."""
    print("\n" + "=" * 60)
    print("4. TYPEVAR / GENERIC")
    print("=" * 60)

    # Stack[int]
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(f"Stack[int]: pop={int_stack.pop()}, peek={int_stack.peek()}")

    # Stack[str]
    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(f"Stack[str]: pop={str_stack.pop()}")

    # Generic функция
    print(f"first([1,2,3]): {first([1, 2, 3])}")
    print(f"first(['a','b']): {first(['a', 'b'])}")
    print(f"first([]): {first([])}")


# =============================================================================
# 5. MYMY / PYRIGHT
# =============================================================================

MYPY_INFO = """
╔══════════════════════════════════════════════════════════════════╗
║  СТАТИЧЕСКАЯ ПРОВЕРКА ТИПОВ                                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Python НЕ проверяет type hints во время выполнения.             ║
║  Для проверки нужны статические анализаторы:                     ║
║                                                                  ║
║  mypy:                                                           ║
║    pip install mypy                                               ║
║    mypy script.py                                                 ║
║    mypy src/ --strict                                             ║
║                                                                  ║
║  pyright (VSCode по умолчанию):                                   ║
║    pip install pyright                                            ║
║    pyright script.py                                              ║
║                                                                  ║
║  ruff (линтер с проверкой типов):                                 ║
║    pip install ruff                                               ║
║    ruff check script.py                                           ║
║                                                                  ║
║  Конфигурация (pyproject.toml):                                   ║
║    [tool.mypy]                                                    ║
║    strict = true                                                  ║
║    [[tool.mypy.overrides]]                                        ║
║    module = "tests.*"                                             ║
║    ignore_errors = true                                           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""


def mypy_demo():
    """Информация о mypy/pyright."""
    print("\n" + "=" * 60)
    print("5. MYPY / PYRIGHT")
    print("=" * 60)
    print(MYPY_INFO)


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    basic_types_demo()
    type_aliases_demo()
    typeddict_protocol_demo()
    generic_demo()
    mypy_demo()

    print("=" * 60)
    print("✅ УРОК 26 ЗАВЕРШЁН: TYPE HINTS ОСВОЕНЫ!")
    print("