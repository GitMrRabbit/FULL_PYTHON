# 🏷️ Урок 26: Type Hints (Аннотации типов)

## 📖 Теория

Type hints — подсказки типов, которые Python игнорирует при выполнении, но которые проверяются статическими анализаторами (mypy, pyright).

---

## 🔹 Базовые типы

```python
def greet(name: str, age: int) -> str:
    return f"{name}, {age} лет"

x: int = 42
names: list[str] = ["Анна", "Борис"]          # Python 3.9+
user: dict[str, any] = {"name": "Анна"}
point: tuple[float, float] = (3.0, 4.0)
tags: set[str] = {"python", "testing"}
```

---

## 🔹 Union, Optional, Any

```python
value: str | None = None            # Python 3.10+ (вместо Optional[str])
result: int | str = "error"         # Union[int, str]
data: Any = "что угодно"            # Отключает проверку типа!
```

---

## 🔹 Callable, TypeAlias, NewType

```python
# Callable — функция
Comparator = Callable[[int, int], bool]
def sort(items: list[int], cmp: Comparator) -> list[int]: ...

# TypeAlias — псевдоним
UserId: TypeAlias = int

# NewType — отдельный тип (строгая проверка mypy)
UserID = NewType("UserID", int)
```

---

## 🔹 TypedDict, Protocol

```python
class UserDict(TypedDict):    # Словарь известной структуры
    name: str
    age: int

class Drawable(Protocol):      # Структурная типизация
    def draw(self) -> str: ...
    def area(self) -> float: ...
```

---

## 🔹 Generic / TypeVar

```python
T = TypeVar("T")

class Stack(Generic[T]):       # Обобщённый стек
    def push(self, item: T) -> None: ...
    def pop(self) -> T | None: ...

int_stack: Stack[int] = Stack()
str_stack: Stack[str] = Stack()
```

---

## 🔹 Проверка типов

```bash
pip install mypy
mypy script.py --strict
```

Type hints **не проверяются** во время выполнения — только статическими анализаторами!

---

## 🧪 Упражнения

1. Добавьте type hints ко всем функциям в существующем проекте
2. Создайте обобщённый класс `Repository[T]` для работы с хранилищем
3. Используйте Protocol для определения интерфейса логгера
4. Запустите mypy на проекте и исправьте все ошибки
