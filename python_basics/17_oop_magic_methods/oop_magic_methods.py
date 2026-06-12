"""
Урок 17: Магические методы (Dunder Methods)
============================================

Магические методы (они же dunder-методы, от "double underscore") —
специальные методы с именами вида __имя__, которые Python вызывает
автоматически в определённых ситуациях.

Темы:
  - __len__, __getitem__, __setitem__, __delitem__ — эмуляция коллекций
  - __iter__, __next__ — итерация
  - __enter__, __exit__ — контекстные менеджеры
  - __call__ — вызываемые объекты
  - __eq__, __lt__, __gt__, __hash__ — сравнение и хеширование
  - __add__, __sub__, __mul__ — арифметические операции
  - __str__, __repr__ — строковое представление
  - __bool__ — преобразование в bool
  - __getattr__, __setattr__, __delattr__ — доступ к атрибутам
"""

import time
from typing import Any


# =============================================================================
# 1. __len__, __getitem__, __setitem__ — ЭМУЛЯЦИЯ КОЛЛЕКЦИЙ
# =============================================================================

class Playlist:
    """Эмуляция списка воспроизведения: можно len(), [], for ... in ..."""

    def __init__(self, name: str, songs: list[str] | None = None):
        self.name = name
        self._songs: list[str] = songs or []

    def __len__(self) -> int:
        """Вызывается: len(playlist)."""
        return len(self._songs)

    def __getitem__(self, index: int | slice) -> str | list[str]:
        """
        Вызывается: playlist[0], playlist[1:3].

        Поддержка как индекса, так и среза!
        """
        if isinstance(index, slice):
            return self._songs[index]
        return self._songs[index]

    def __setitem__(self, index: int, value: str) -> None:
        """Вызывается: playlist[0] = 'New Song'."""
        self._songs[index] = value

    def __delitem__(self, index: int) -> None:
        """Вызывается: del playlist[0]."""
        del self._songs[index]

    def __contains__(self, item: str) -> bool:
        """Вызывается: 'Song' in playlist."""
        return item in self._songs

    def __reversed__(self):
        """Вызывается: reversed(playlist)."""
        return reversed(self._songs)

    def add(self, song: str) -> None:
        self._songs.append(song)

    def __repr__(self) -> str:
        return f"Playlist({self.name!r}, {self._songs})"


def collection_emulation_demo():
    """Демонстрация эмуляции коллекций."""
    print("=" * 60)
    print("1. ЭМУЛЯЦИЯ КОЛЛЕКЦИЙ (__len__, __getitem__)")
    print("=" * 60)

    pl = Playlist("Мой плейлист", ["Song A", "Song B", "Song C", "Song D"])

    # len()
    print(f"len(pl) = {len(pl)}")

    # Индексация
    print(f"pl[0] = {pl[0]}")
    print(f"pl[-1] = {pl[-1]}")

    # Срезы
    print(f"pl[1:3] = {pl[1:3]}")

    # Присваивание
    pl[0] = "New Song"
    print(f"После pl[0] = 'New Song': {pl[0]}")

    # in
    print(f"'Song B' in pl: {'Song B' in pl}")

    # Итерация (работает благодаря __getitem__!)
    print("Итерация:")
    for song in pl:
        print(f"  - {song}")

    # reversed
    print("Реверс:")
    for song in reversed(pl):
        print(f"  - {song}")


# =============================================================================
# 2. __iter__, __next__ — ИТЕРАТОРЫ
# =============================================================================

class Countdown:
    """Итератор обратного отсчёта."""

    def __init__(self, start: int):
        self._current = start

    def __iter__(self):
        """Возвращает итератор (обычно self)."""
        return self

    def __next__(self):
        """Возвращает следующий элемент или StopIteration."""
        if self._current < 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


def iterator_demo():
    """Демонстрация итераторов."""
    print("\n" + "=" * 60)
    print("2. ИТЕРАТОРЫ (__iter__, __next__)")
    print("=" * 60)

    print("Countdown(5):", end=" ")
    for n in Countdown(5):
        print(n, end=" ")
    print()

    # Ручной вызов
    cd = Countdown(3)
    iterator = iter(cd)
    print(f"next: {next(iterator)}")
    print(f"next: {next(iterator)}")
    print(f"next: {next(iterator)}")
    print(f"next: {next(iterator)}")  # 0
    try:
        next(iterator)  # StopIteration
    except StopIteration:
        print("StopIteration!")


# =============================================================================
# 3. __enter__, __exit__ — КОНТЕКСТНЫЕ МЕНЕДЖЕРЫ
# =============================================================================

class Timer:
    """Измеряет время выполнения блока кода. Контекстный менеджер."""

    def __init__(self, label: str = "Время"):
        self.label = label
        self._start: float = 0.0
        self._elapsed: float = 0.0

    def __enter__(self):
        """Вход в контекст: with Timer() as t: ..."""
        self._start = time.perf_counter()
        return self  # Будет связано с 'as t'

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Выход из контекста (всегда, даже при исключении!).
        Если вернуть True — исключение подавляется.
        """
        self._elapsed = time.perf_counter() - self._start
        print(f"⏱ {self.label}: {self._elapsed:.4f} сек")

        # Не подавляем исключения
        return False

    @property
    def elapsed(self) -> float:
        return self._elapsed


class Transaction:
    """
    Транзакция: commit при успехе, rollback при ошибке.
    Демонстрирует __exit__ с обработкой исключений.
    """

    def __init__(self, name: str):
        self.name = name
        self._committed = False

    def __enter__(self):
        print(f"[TX] BEGIN {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._committed = True
            print(f"[TX] COMMIT {self.name}")
        else:
            print(f"[TX] ROLLBACK {self.name} (причина: {exc_type.__name__})")
        return False  # Пробрасываем исключение дальше


def context_manager_demo():
    """Демонстрация контекстных менеджеров."""
    print("\n" + "=" * 60)
    print("3. КОНТЕКСТНЫЕ МЕНЕДЖЕРЫ (__enter__, __exit__)")
    print("=" * 60)

    # Timer
    with Timer("Вычисление") as t:
        total = sum(range(1_000_000))

    # Transaction — успех
    with Transaction("Успешная операция"):
        print("  Выполняю работу...")

    # Transaction — ошибка
    try:
        with Transaction("Операция с ошибкой"):
            print("  Работаю...")
            raise ValueError("Что-то пошло не так!")
    except ValueError:
        print("  (Исключение перехвачено снаружи)")


# =============================================================================
# 4. __call__ — ВЫЗЫВАЕМЫЕ ОБЪЕКТЫ
# =============================================================================

class Multiplier:
    """Объект можно вызывать как функцию."""

    def __init__(self, factor: int):
        self.factor = factor

    def __call__(self, x: int) -> int:
        return x * self.factor


class Validator:
    """Цепочка валидаторов как вызываемый объект."""

    def __init__(self):
        self._rules: list[callable] = []

    def add_rule(self, rule: callable) -> "Validator":
        self._rules.append(rule)
        return self  # Fluent API

    def __call__(self, value: Any) -> list[str]:
        """Вызов: validator(value) → список ошибок."""
        errors = []
        for rule in self._rules:
            error = rule(value)
            if error:
                errors.append(error)
        return errors


def callable_objects_demo():
    """Демонстрация вызываемых объектов."""
    print("\n" + "=" * 60)
    print("4. ВЫЗЫВАЕМЫЕ ОБЪЕКТЫ (__call__)")
    print("=" * 60)

    double = Multiplier(2)
    triple = Multiplier(3)
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")

    # Валидатор как вызываемый объект
    def not_empty(v): return "Не может быть пустым" if not v else None
    def min_length(n): return lambda v: f"Минимум {n} символов" if len(v) < n else None

    validator = Validator()
    validator.add_rule(not_empty).add_rule(min_length(5))

    print(f"\nВалидация '': {validator('')}")
    print(f"Валидация 'abc': {validator('abc')}")
    print(f"Валидация 'hello': {validator('hello')}")


# =============================================================================
# 5. АРИФМЕТИЧЕСКИЕ ОПЕРАЦИИ
# =============================================================================

class Vector:
    """2D-вектор с поддержкой +, -, *, ==."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        """self + other"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        """self - other"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        """self * scalar (только vector * число)"""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        """scalar * self (если левый операнд не Vector)"""
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector":
        """-self"""
        return Vector(-self.x, -self.y)

    def __abs__(self) -> float:
        """abs(vector) — длина вектора."""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __eq__(self, other: "Vector") -> bool:
        """self == other"""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Для использования в set/dict ключах."""
        return hash((self.x, self.y))

    def __bool__(self) -> bool:
        """bool(vector) — True если не нулевой вектор."""
        return self.x != 0 or self.y != 0

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"


def arithmetic_operations_demo():
    """Демонстрация арифметических операций."""
    print("\n" + "=" * 60)
    print("5. АРИФМЕТИЧЕСКИЕ ОПЕРАЦИИ")
    print("=" * 60)

    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"3 * v1 = {3 * v1}")          # __rmul__
    print(f"-v1 = {-v1}")                # __neg__
    print(f"abs(v1) = {abs(v1):.2f}")    # __abs__
    print(f"v1 == v2: {v1 == v2}")       # __eq__
    print(f"bool(v1): {bool(v1)}")       # __bool__
    print(f"bool(Vector(0,0)): {bool(Vector(0, 0))}")

    # Хеширование позволяет использовать Vector в set/dict
    vectors = {Vector(3, 4), Vector(1, 2), Vector(3, 4)}
    print(f"set из векторов: {vectors}")  # Только 2 уникальных


# =============================================================================
# 6. __getattr__, __setattr__, __delattr__
# =============================================================================

class LazyLoader:
    """
    «Ленивая» загрузка атрибутов.
    Если атрибут не найден, загружает его из БД/API.
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        self._cache: dict[str, Any] = {"id": user_id}
        self._access_count: dict[str, int] = {}

    def __getattr__(self, name: str) -> Any:
        """
        Вызывается, только если атрибут НЕ найден обычным способом.
        """
        if name.startswith("_"):
            raise AttributeError(name)

        # Симулируем загрузку из БД
        print(f"  [LazyLoader] Загружаю '{name}' для user#{self.user_id}...")
        # В реальном коде здесь был бы запрос к БД
        value = f"значение_{name}_для_user_{self.user_id}"
        self._cache[name] = value
        return value

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Вызывается при ЛЮБОМ присваивании атрибута.
        """
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self.__dict__.setdefault("_cache", {})[name] = value
            super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        if name in self._cache:
            del self._cache[name]
        super().__delattr__(name)


def attribute_access_demo():
    """Демонстрация управления доступом к атрибутам."""
    print("\n" + "=" * 60)
    print("6. ДОСТУП К АТРИБУТАМ (__getattr__, __setattr__)")
    print("=" * 60)

    user = LazyLoader(42)

    # Существующий атрибут
    print(f"user.user_id = {user.user_id}")

    # Несуществующий → __getattr__
    print(f"user.name = {user.name}")
    print(f"user.email = {user.email}")

    # Теперь они в __dict__ и __getattr__ больше не вызывается
    print(f"user.name (повторно) = {user.name}")


# =============================================================================
# 7. СВОДНАЯ ТАБЛИЦА МАГИЧЕСКИХ МЕТОДОВ
# =============================================================================

MAGIC_METHODS_TABLE = """
╔══════════════════════════════════════════════════════════════════╗
║               СВОДКА МАГИЧЕСКИХ МЕТОДОВ                          ║
╠══════════════╦═══════════════════════════════════════════════════╣
║ Категория    ║ Методы                                           ║
╠══════════════╬═══════════════════════════════════════════════════╣
║ Создание     ║ __init__, __new__, __del__                        ║
║ Строки       ║ __str__, __repr__, __format__, __bytes__          ║
║ Коллекции    ║ __len__, __getitem__, __setitem__, __delitem__,   ║
║              ║ __contains__, __reversed__, __missing__           ║
║ Итерация     ║ __iter__, __next__                                ║
║ Вызов        ║ __call__                                          ║
║ Контекст     ║ __enter__, __exit__                               ║
║ Сравнение    ║ __eq__, __ne__, __lt__, __gt__, __le__, __ge__,   ║
║              ║ __hash__                                          ║
║ Арифметика   ║ __add__, __sub__, __mul__, __truediv__,           ║
║              ║ __floordiv__, __mod__, __pow__, __neg__           ║
║ Атрибуты     ║ __getattr__, __setattr__, __delattr__,            ║
║              ║ __getattribute__, __dir__                         ║
║ Преобр-ние   ║ __bool__, __int__, __float__, __complex__         ║
╚══════════════╩═══════════════════════════════════════════════════╝
"""


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    collection_emulation_demo()
    iterator_demo()
    context_manager_demo()
    callable_objects_demo()
    arithmetic_operations_demo()
    attribute_access_demo()

    print("\n" + MAGIC_METHODS_TABLE)

    print("\n" + "=" * 60)
    print("✅ УРОК 17 ЗАВЕРШЁН: МАГИЧЕСКИЕ МЕТОДЫ ОСВОЕНЫ!")
    print("=" * 60)
