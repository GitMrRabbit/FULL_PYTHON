"""
Урок 15: ООП — Основы (Классы и Объекты)
=========================================

Темы:
  - Класс и объект (экземпляр)
  - __init__ — конструктор
  - self — ссылка на экземпляр
  - Атрибуты экземпляра и класса
  - Методы экземпляра
  - __str__ и __repr__ — строковое представление
  - Инкапсуляция (public, _protected, __private)
  - @dataclass — классы данных (Python 3.7+)
"""

from dataclasses import dataclass, field
from typing import ClassVar


# =============================================================================
# 1. БАЗОВЫЙ КЛАСС И ОБЪЕКТ
# =============================================================================

class Person:
    """
    Простой класс Person.

    Атрибуты класса (class attributes) — общие для всех экземпляров.
    Атрибуты экземпляра (instance attributes) — уникальные для каждого.
    """

    # Атрибут класса (общий для всех)
    species: ClassVar[str] = "Homo Sapiens"
    count: ClassVar[int] = 0          # Счётчик созданных экземпляров

    def __init__(self, name: str, age: int):
        """
        Конструктор. Вызывается при создании объекта: Person("Анна", 28).

        self — ссылка на конкретный экземпляр.
        """
        self.name = name        # Атрибут экземпляра
        self.age = age          # Атрибут экземпляра
        Person.count += 1       # Увеличиваем счётчик класса

    def greet(self) -> str:
        """Метод экземпляра. Первый параметр всегда self."""
        return f"Привет, я {self.name}, мне {self.age} лет."

    def birthday(self) -> None:
        """Увеличивает возраст на 1."""
        self.age += 1
        print(f"🎂 С днём рождения, {self.name}! Теперь тебе {self.age}.")

    # --- Строковое представление ---

    def __str__(self) -> str:
        """
        Для пользователей: str(obj), print(obj).
        Должно быть читаемым и информативным.
        """
        return f"Person(name='{self.name}', age={self.age})"

    def __repr__(self) -> str:
        """
        Для разработчиков: repr(obj), в консоли.
        В идеале — код, который воссоздаст объект.
        """
        return f"Person(name={self.name!r}, age={self.age!r})"


def basic_class_demo():
    """Демонстрация базового класса."""
    print("=" * 60)
    print("1. БАЗОВЫЙ КЛАСС И ОБЪЕКТ")
    print("=" * 60)

    # Создание объектов (экземпляров)
    alice = Person("Алиса", 28)
    bob = Person("Боб", 35)

    # Доступ к атрибутам
    print(f"alice.name = {alice.name}")
    print(f"bob.age = {bob.age}")

    # Вызов методов
    print(f"alice.greet() → {alice.greet()}")
    alice.birthday()

    # Атрибут класса доступен через экземпляр и через класс
    print(f"alice.species = {alice.species}")
    print(f"Person.species = {Person.species}")
    print(f"Всего создано: {Person.count} чел.")

    # __str__ vs __repr__
    print(f"str(alice)  = {str(alice)}")
    print(f"repr(alice) = {repr(alice)}")

    # Проверка типа
    print(f"isinstance(alice, Person) = {isinstance(alice, Person)}")
    print(f"isinstance(alice, object) = {isinstance(alice, object)}")


# =============================================================================
# 2. ИНКАПСУЛЯЦИЯ (public, _protected, __private)
# =============================================================================

class BankAccount:
    """Демонстрация инкапсуляции: public, _protected, __private."""

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner              # public — доступен всем
        self._bank = "MyBank"           # _protected — соглашение: не трогать снаружи
        self.__balance = balance        # __private — name mangling (доступ через _BankAccount__balance)

    def deposit(self, amount: float) -> None:
        """Публичный метод для пополнения."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.__balance += amount
        print(f"[+] Пополнение {amount:.2f} ₽. Баланс: {self.__balance:.2f} ₽")

    def withdraw(self, amount: float) -> bool:
        """Публичный метод для снятия."""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self.__balance:
            print(f"[-] Недостаточно средств! Баланс: {self.__balance:.2f} ₽")
            return False
        self.__balance -= amount
        print(f"[-] Снятие {amount:.2f} ₽. Баланс: {self.__balance:.2f} ₽")
        return True

    def get_balance(self) -> float:
        """Геттер для приватного поля."""
        return self.__balance

    def __str__(self) -> str:
        return f"BankAccount(owner='{self.owner}', balance={self.__balance:.2f})"


def encapsulation_demo():
    """Демонстрация инкапсуляции."""
    print("\n" + "=" * 60)
    print("2. ИНКАПСУЛЯЦИЯ")
    print("=" * 60)

    acc = BankAccount("Анна", 1000.0)

    # Публичный доступ
    print(f"acc.owner = {acc.owner}")
    acc.owner = "Анна С."       # Можно менять
    print(f"acc.owner = {acc.owner}")

    # _protected — технически доступен, но не рекомендуется
    print(f"acc._bank = {acc._bank}")   # Работает, но не делайте так!

    # __private — name mangling
    try:
        print(acc.__balance)            # AttributeError!
    except AttributeError:
        print("[!] AttributeError: __balance недоступен напрямую")

    # Но можно обойти (НЕ ДЕЛАЙТЕ ТАК!)
    print(f"Обход: acc._BankAccount__balance = {acc._BankAccount__balance}")

    # Правильный доступ через методы
    print(f"acc.get_balance() = {acc.get_balance()}")
    acc.deposit(500)
    acc.withdraw(200)
    acc.withdraw(2000)  # Недостаточно средств

    print(f"Итог: {acc}")


# =============================================================================
# 3. @DATACLASS — КЛАССЫ ДАННЫХ (Python 3.7+)
# =============================================================================

@dataclass
class Product:
    """
    Декоратор @dataclass автоматически генерирует:
      - __init__()
      - __repr__()
      - __eq__()
      - (опционально) __hash__(), __lt__(), и т.д.
    """
    name: str
    price: float
    in_stock: bool = True
    tags: list[str] = field(default_factory=list)  # ВАЖНО: default_factory для изменяемых типов!

    def total_price(self, quantity: int) -> float:
        """Метод экземпляра (не генерируется автоматически)."""
        return self.price * quantity

    def __post_init__(self):
        """Вызывается после __init__. Например, для валидации."""
        if self.price < 0:
            raise ValueError(f"Цена не может быть отрицательной: {self.price}")


@dataclass(frozen=True)  # Неизменяемый (read-only) dataclass
class Point:
    """Неизменяемая точка (как namedtuple, но с методами)."""
    x: float
    y: float

    def distance_to_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5


def dataclass_demo():
    """Демонстрация @dataclass."""
    print("\n" + "=" * 60)
    print("3. @DATACLASS")
    print("=" * 60)

    # Создание
    p1 = Product("Ноутбук", 50000.0)
    p2 = Product("Мышь", 2000.0, in_stock=False, tags=["беспроводная", "usb-c"])
    print(p1)  # Автоматический __repr__
    print(p2)

    # Сравнение (автоматический __eq__)
    p3 = Product("Ноутбук", 50000.0)
    print(f"p1 == p3: {p1 == p3}")  # True (сравнение по полям)

    # Методы
    print(f"2x {p1.name} = {p1.total_price(2):.2f} ₽")

    # Неизменяемый dataclass
    pt = Point(3.0, 4.0)
    print(f"Point: {pt}, расстояние до (0,0): {pt.distance_to_origin()}")
    try:
        pt.x = 10.0  # FrozenInstanceError!
    except Exception as e:
        print(f"[!] {type(e).__name__}: {e}")

    # Ошибка валидации
    try:
        Product("Брак", -100)
    except ValueError as e:
        print(f"[!] {e}")


# =============================================================================
# 4. ПРАКТИЧЕСКИЙ ПРИМЕР: БИБЛИОТЕКА
# =============================================================================

class Book:
    """Модель книги."""

    def __init__(self, title: str, author: str, isbn: str, year: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self._is_borrowed = False

    def borrow(self) -> bool:
        if self._is_borrowed:
            return False
        self._is_borrowed = True
        return True

    def return_book(self) -> None:
        self._is_borrowed = False

    @property
    def is_available(self) -> bool:
        return not self._is_borrowed

    def __str__(self) -> str:
        status = "✅" if self.is_available else "❌"
        return f"{status} {self.title} — {self.author} ({self.year})"

    def __repr__(self) -> str:
        return f"Book(title={self.title!r}, author={self.author!r})"


class Library:
    """Управление коллекцией книг."""

    def __init__(self, name: str):
        self.name = name
        self._books: list[Book] = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)
        print(f"[+] Добавлена: {book.title}")

    def find_by_author(self, author: str) -> list[Book]:
        return [b for b in self._books if b.author.lower() == author.lower()]

    def find_available(self) -> list[Book]:
        return [b for b in self._books if b.is_available]

    def borrow_book(self, isbn: str) -> bool:
        for book in self._books:
            if book.isbn == isbn and book.borrow():
                print(f"[✓] Выдана: {book.title}")
                return True
        print(f"[✗] Книга с ISBN {isbn} недоступна")
        return False

    def list_all(self) -> None:
        print(f"\n📚 Библиотека «{self.name}»:")
        for book in self._books:
            print(f"  {book}")

    def __len__(self) -> int:
        return len(self._books)

    def __contains__(self, isbn: str) -> bool:
        return any(b.isbn == isbn for b in self._books)


def practical_example():
    """Практический пример: библиотека."""
    print("\n" + "=" * 60)
    print("4. ПРАКТИЧЕСКИЙ ПРИМЕР: БИБЛИОТЕКА")
    print("=" * 60)

    lib = Library("Главная библиотека")

    lib.add_book(Book("Война и мир", "Толстой Л.Н.", "978-5-389-12345", 1869))
    lib.add_book(Book("Преступление и наказание", "Достоевский Ф.М.", "978-5-389-12346", 1866))
    lib.add_book(Book("Анна Каренина", "Толстой Л.Н.", "978-5-389-12347", 1877))

    lib.list_all()

    print(f"\nВсего книг: {len(lib)}")
    print(f"ISBN 978-5-389-12345 в библиотеке: {'978-5-389-12345' in lib}")

    lib.borrow_book("978-5-389-12345")
    lib.borrow_book("978-5-389-12345")  # Уже выдана

    print(f"\nДоступные книги:")
    for book in lib.find_available():
        print(f"  {book}")

    print(f"\nКниги Толстого:")
    for book in lib.find_by_author("Толстой Л.Н."):
        print(f"  {book}")


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    basic_class_demo()
    encapsulation_demo()
    dataclass_demo()
    practical_example()

    print("\n" + "=" * 60)
    print("✅ УРОК 15 ЗАВЕРШЁН: ООП ОСНОВЫ ОСВОЕНЫ!")
    print("=" * 60)
