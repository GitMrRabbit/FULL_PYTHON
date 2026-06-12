"""
Урок 18: ООП — Свойства, classmethod, staticmethod
====================================================

Темы:
  - @property — геттер (вычисляемые атрибуты)
  - @name.setter — сеттер (валидация при присваивании)
  - @name.deleter — удаление атрибута
  - Инкапсуляция с @property
  - @classmethod — методы класса (cls вместо self)
  - @staticmethod — статические методы (ни self, ни cls)
  - __slots__ — оптимизация памяти
"""

from datetime import datetime, date
from typing import ClassVar


# =============================================================================
# 1. @PROPERTY — ВЫЧИСЛЯЕМЫЕ АТРИБУТЫ
# =============================================================================

class Circle:
    """Демонстрация @property для вычисляемых атрибутов."""

    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        """Геттер: circle.radius (без скобок!)."""
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        """Сеттер: circle.radius = 5 (с валидацией)."""
        if value < 0:
            raise ValueError("Радиус не может быть отрицательным")
        self._radius = value

    @radius.deleter
    def radius(self) -> None:
        """Делетер: del circle.radius."""
        print("Сброс радиуса к 0")
        self._radius = 0

    @property
    def diameter(self) -> float:
        """Вычисляемое свойство (только для чтения)."""
        return self._radius * 2

    @property
    def area(self) -> float:
        """Вычисляемое свойство."""
        import math
        return math.pi * self._radius ** 2

    def __repr__(self) -> str:
        return f"Circle(radius={self._radius})"


def property_demo():
    """Демонстрация @property."""
    print("=" * 60)
    print("1. @PROPERTY")
    print("=" * 60)

    c = Circle(5)
    print(f"c = {c}")

    # Геттер — без скобок
    print(f"c.radius = {c.radius}")
    print(f"c.diameter = {c.diameter}")
    print(f"c.area = {c.area:.2f}")

    # Сеттер — с валидацией
    c.radius = 10
    print(f"После c.radius = 10: {c}, area = {c.area:.2f}")

    try:
        c.radius = -1  # ValueError!
    except ValueError as e:
        print(f"[!] {e}")

    # Делетер
    del c.radius
    print(f"После del c.radius: {c}")


# =============================================================================
# 2. ИНКАПСУЛЯЦИЯ С @PROPERTY
# =============================================================================

class Temperature:
    """Хранит температуру в Кельвинах, но позволяет задавать в Цельсиях/Фаренгейтах."""

    def __init__(self, kelvin: float = 273.15):
        self._kelvin = kelvin

    @property
    def kelvin(self) -> float:
        return self._kelvin

    @kelvin.setter
    def kelvin(self, value: float) -> None:
        if value < 0:
            raise ValueError("Температура в Кельвинах не может быть отрицательной")
        self._kelvin = value

    @property
    def celsius(self) -> float:
        """Цельсий: K - 273.15."""
        return self._kelvin - 273.15

    @celsius.setter
    def celsius(self, value: float) -> None:
        self.kelvin = value + 273.15

    @property
    def fahrenheit(self) -> float:
        """Фаренгейт: (K - 273.15) * 9/5 + 32."""
        return self.celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5 / 9

    def __repr__(self) -> str:
        return (f"Temperature({self.kelvin:.2f}K = "
                f"{self.celsius:.2f}°C = {self.fahrenheit:.2f}°F)")


def encapsulation_demo():
    """Демонстрация инкапсуляции с @property."""
    print("\n" + "=" * 60)
    print("2. ИНКАПСУЛЯЦИЯ С @PROPERTY")
    print("=" * 60)

    t = Temperature()
    print(f"Начальная: {t}")

    t.celsius = 100
    print(f"После t.celsius = 100: {t}")

    t.fahrenheit = 32
    print(f"После t.fahrenheit = 32: {t}")

    t.kelvin = 373.15
    print(f"После t.kelvin = 373.15: {t}")


# =============================================================================
# 3. @CLASSMETHOD И @STATICMETHOD
# =============================================================================

class Person:
    """Демонстрация @classmethod и @staticmethod."""

    population: ClassVar[int] = 0
    VALID_GENDERS: ClassVar[frozenset] = frozenset({"male", "female", "other"})

    def __init__(self, name: str, birth_year: int, gender: str = "other"):
        self.name = name
        self.birth_year = birth_year
        self.gender = gender if gender in self.VALID_GENDERS else "other"
        Person.population += 1

    @property
    def age(self) -> int:
        """Вычисляемый возраст (зависит от текущего года)."""
        return datetime.now().year - self.birth_year

    @classmethod
    def from_birth_date(cls, name: str, birth_date: str, gender: str = "other") -> "Person":
        """
        Альтернативный конструктор: Person.from_birth_date("Анна", "1995-05-15").
        cls — сам класс Person (не экземпляр!).
        """
        dt = datetime.strptime(birth_date, "%Y-%m-%d")
        return cls(name=name, birth_year=dt.year, gender=gender)

    @classmethod
    def get_population(cls) -> int:
        """Метод класса: доступен без создания экземпляра."""
        return cls.population

    @staticmethod
    def is_adult_age(age: int) -> bool:
        """
        Статический метод: не принимает ни self, ни cls.
        Просто функция, логически связанная с классом.
        """
        return age >= 18

    @staticmethod
    def validate_name(name: str) -> bool:
        """Валидация имени (статический метод)."""
        return bool(name) and len(name.strip()) >= 2

    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age}, gender={self.gender})"


def classmethod_staticmethod_demo():
    """Демонстрация @classmethod и @staticmethod."""
    print("\n" + "=" * 60)
    print("3. @CLASSMETHOD И @STATICMETHOD")
    print("=" * 60)

    # Обычный конструктор
    p1 = Person("Борис", 1990, "male")
    print(f"Обычный: {p1}")

    # Альтернативный конструктор
    p2 = Person.from_birth_date("Анна", "1995-05-15", "female")
    print(f"From date: {p2}")

    # @classmethod без экземпляра
    print(f"Население: {Person.get_population()}")

    # @staticmethod
    print(f"is_adult_age(16): {Person.is_adult_age(16)}")
    print(f"is_adult_age(25): {Person.is_adult_age(25)}")
    print(f"validate_name(''):  {Person.validate_name('')}")
    print(f"validate_name('Анна'): {Person.validate_name('Анна')}")


# =============================================================================
# 4. __SLOTS__ — ОПТИМИЗАЦИЯ ПАМЯТИ
# =============================================================================

class RegularPoint:
    """Обычный класс с __dict__ (каждый экземпляр хранит словарь атрибутов)."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class SlottedPoint:
    """Класс с __slots__ (фиксированный набор атрибутов, нет __dict__)."""

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


def slots_demo():
    """Демонстрация __slots__."""
    print("\n" + "=" * 60)
    print("4. __SLOTS__ — ОПТИМИЗАЦИЯ ПАМЯТИ")
    print("=" * 60)

    import sys

    reg = RegularPoint(1.0, 2.0)
    slot = SlottedPoint(1.0, 2.0)

    print(f"RegularPoint размер: {sys.getsizeof(reg)} байт (+ __dict__)")
    print(f"SlottedPoint размер: {sys.getsizeof(slot)} байт (без __dict__)")

    # У RegularPoint есть __dict__
    print(f"reg.__dict__: {reg.__dict__}")

    # У SlottedPoint нет __dict__
    # print(slot.__dict__)  # AttributeError!
    print(f"hasattr(slot, '__dict__'): {hasattr(slot, '__dict__')}")

    # Нельзя добавить новые атрибуты
    try:
        slot.z = 3.0  # AttributeError!
    except AttributeError:
        print("[!] AttributeError: нельзя добавить новый атрибут к slotted классу")

    # Но можно изменить существующие
    slot.x = 10.0
    print(f"slot.x = {slot.x}  # Изменить существующий — можно")


# =============================================================================
# 5. ПРАКТИЧЕСКИЙ ПРИМЕР: ВАЛИДИРУЕМАЯ МОДЕЛЬ
# =============================================================================

class BankAccount:
    """
    Банковский счёт с full-инкапсуляцией через @property.
    Все изменения проходят валидацию.
    """

    MIN_BALANCE: ClassVar[float] = -1000.0  # Овердрафт
    INTEREST_RATE: ClassVar[float] = 0.05    # 5% годовых

    def __init__(self, owner: str, initial_balance: float = 0.0):
        self._owner = owner
        self._balance = initial_balance
        self._transactions: list[tuple[datetime, str, float]] = []
        self._opened_at = datetime.now()

    # --- owner (только для чтения после создания) ---
    @property
    def owner(self) -> str:
        return self._owner

    # --- balance (с валидацией) ---
    @property
    def balance(self) -> float:
        return self._balance

    # --- opened_at (только для чтения) ---
    @property
    def opened_at(self) -> datetime:
        return self._opened_at

    # --- age (вычисляемое) ---
    @property
    def account_age_days(self) -> float:
        return (datetime.now() - self._opened_at).days

    # --- Методы ---
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._balance += amount
        self._log_transaction("DEPOSIT", amount)

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if self._balance - amount < self.MIN_BALANCE:
            print(f"[!] Недостаточно средств. Баланс: {self._balance:.2f}, "
                  f"лимит: {self.MIN_BALANCE:.2f}")
            return False
        self._balance -= amount
        self._log_transaction("WITHDRAW", -amount)
        return True

    def _log_transaction(self, type_: str, amount: float) -> None:
        self._transactions.append((datetime.now(), type_, amount))

    @property
    def last_transactions(self, n: int = 5) -> list:
        """Последние n транзакций."""
        return self._transactions[-n:]

    @classmethod
    def create_savings_account(cls, owner: str, initial: float = 1000.0) -> "BankAccount":
        """Фабричный метод: создать накопительный счёт."""
        account = cls(owner, initial)
        print(f"[✓] Создан накопительный счёт для {owner} с балансом {initial:.2f} ₽")
        return account

    def __repr__(self) -> str:
        return (f"BankAccount(owner='{self.owner}', "
                f"balance={self.balance:.2f}, "
                f"age={self.account_age_days:.0f}d)")


def practical_example():
    """Практический пример: банковский счёт."""
    print("\n" + "=" * 60)
    print("5. ПРАКТИЧЕСКИЙ ПРИМЕР: БАНКОВСКИЙ СЧЁТ")
    print("=" * 60)

    acc = BankAccount.create_savings_account("Анна", 5000)
    print(f"Счёт: {acc}")

    acc.deposit(1500)
    acc.withdraw(2000)
    acc.withdraw(10000)  # Превышение

    print(f"\nИтоговый баланс: {acc.balance:.2f} ₽")
    print("Последние транзакции:")
    for dt, type_, amount in acc.last_transactions:
        print(f"  {dt.strftime('%H:%M:%S')} | {type_:8s} | {amount:+.2f} ₽")


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    property_demo()
    encapsulation_demo()
    classmethod_staticmethod_demo()
    slots_demo()
    practical_example()

    print("\n" + "=" * 60)
    print("✅ УРОК 18 ЗАВЕРШЁН: PROPERTIES, CLASSMETHOD, STATICMETHOD!")
    print("=" * 60)
