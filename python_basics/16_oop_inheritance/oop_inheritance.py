"""
Урок 16: ООП — Наследование и Полиморфизм
==========================================

Темы:
  - Простое наследование (class Child(Parent))
  - super() — вызов методов родителя
  - Переопределение методов (method overriding)
  - Множественное наследование
  - MRO (Method Resolution Order) — порядок разрешения методов
  - Абстрактные классы (abc.ABC, @abstractmethod)
  - Полиморфизм — "один интерфейс, много реализаций"
  - isinstance() / issubclass()
"""

from abc import ABC, abstractmethod
import math


# =============================================================================
# 1. ПРОСТОЕ НАСЛЕДОВАНИЕ
# =============================================================================

class Animal:
    """Базовый класс (родитель, суперкласс)."""

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    def speak(self) -> str:
        return "..."

    def move(self) -> str:
        return f"{self.name} передвигается"

    def __str__(self) -> str:
        return f"{self.species} по имени {self.name}"


class Dog(Animal):
    """Класс-наследник (дочерний, подкласс)."""

    def __init__(self, name: str, breed: str):
        # Вызов конструктора родителя через super()
        super().__init__(name, species="Собака")
        self.breed = breed          # Новый атрибут

    def speak(self) -> str:
        """Переопределение метода (override)."""
        return "Гав-гав!"

    def fetch(self, item: str) -> str:
        """Метод только у Dog (нет в Animal)."""
        return f"{self.name} приносит {item}"


class Cat(Animal):
    """Ещё один наследник."""

    def __init__(self, name: str, color: str):
        super().__init__(name, species="Кошка")
        self.color = color

    def speak(self) -> str:
        return "Мяу!"

    def purr(self) -> str:
        return f"{self.name} мурлычет"


def simple_inheritance_demo():
    """Демонстрация простого наследования."""
    print("=" * 60)
    print("1. ПРОСТОЕ НАСЛЕДОВАНИЕ")
    print("=" * 60)

    # Создание объектов
    rex = Dog("Рекс", "овчарка")
    murka = Cat("Мурка", "рыжий")

    # Наследованные методы
    print(rex)               # Animal.__str__
    print(f"  move: {rex.move()}")  # Animal.move
    print(f"  speak: {rex.speak()}") # Dog.speak (override)
    print(f"  fetch: {rex.fetch('мячик')}")  # Dog.fetch

    print()
    print(murka)
    print(f"  speak: {murka.speak()}")
    print(f"  purr: {murka.purr()}")

    # Проверки типов
    print(f"\nisinstance(rex, Dog):    {isinstance(rex, Dog)}")     # True
    print(f"isinstance(rex, Animal): {isinstance(rex, Animal)}")  # True
    print(f"isinstance(rex, Cat):    {isinstance(rex, Cat)}")     # False
    print(f"issubclass(Dog, Animal): {issubclass(Dog, Animal)}")  # True


# =============================================================================
# 2. МНОЖЕСТВЕННОЕ НАСЛЕДОВАНИЕ И MRO
# =============================================================================

class Flyable:
    """Примесь (mixin) — добавляет поведение 'летать'."""

    def fly(self) -> str:
        return f"{self.__class__.__name__} летит!"


class Swimmable:
    """Примесь (mixin) — добавляет поведение 'плавать'."""

    def swim(self) -> str:
        return f"{self.__class__.__name__} плывёт!"


class Duck(Animal, Flyable, Swimmable):
    """Множественное наследование: Duck = Animal + Flyable + Swimmable."""

    def __init__(self, name: str):
        super().__init__(name, species="Утка")

    def speak(self) -> str:
        return "Кря-кря!"


class Penguin(Animal, Swimmable):
    """Пингвин плавает, но не летает."""

    def __init__(self, name: str):
        super().__init__(name, species="Пингвин")

    def speak(self) -> str:
        return "Пи-пи!"


def multiple_inheritance_demo():
    """Демонстрация множественного наследования и MRO."""
    print("\n" + "=" * 60)
    print("2. МНОЖЕСТВЕННОЕ НАСЛЕДОВАНИЕ И MRO")
    print("=" * 60)

    donald = Duck("Дональд")
    pingu = Penguin("Пингу")

    print(donald)
    print(f"  speak: {donald.speak()}")
    print(f"  fly: {donald.fly()}")
    print(f"  swim: {donald.swim()}")

    print()
    print(pingu)
    print(f"  speak: {pingu.speak()}")
    print(f"  swim: {pingu.swim()}")
    # pingu.fly()  # AttributeError: Penguin не наследует Flyable!

    # MRO — порядок разрешения методов
    print(f"\nDuck MRO: {[c.__name__ for c in Duck.__mro__]}")
    print(f"Duck.__mro__ = {Duck.__mro__}")


# =============================================================================
# 3. АБСТРАКТНЫЕ КЛАССЫ
# =============================================================================

class Shape(ABC):
    """
    Абстрактный класс — нельзя создать экземпляр напрямую.
    Задаёт интерфейс, который должны реализовать наследники.
    """

    @abstractmethod
    def area(self) -> float:
        """Вычислить площадь."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Вычислить периметр."""
        ...

    def describe(self) -> str:
        """Конкретный метод — доступен всем наследникам."""
        return f"{self.__class__.__name__}: площадь={self.area():.2f}, периметр={self.perimeter():.2f}"


class Circle(Shape):
    """Конкретная реализация Shape."""

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    """Конкретная реализация Shape."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    """Конкретная реализация Shape."""

    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        # Формула Герона
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


def abstract_class_demo():
    """Демонстрация абстрактных классов."""
    print("\n" + "=" * 60)
    print("3. АБСТРАКТНЫЕ КЛАССЫ")
    print("=" * 60)

    # shape = Shape()  # TypeError: Can't instantiate abstract class

    shapes: list[Shape] = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5),
    ]

    # Полиморфизм: единый интерфейс для разных фигур
    for shape in shapes:
        print(f"  {shape.describe()}")


# =============================================================================
# 4. РОМБОВИДНОЕ НАСЛЕДОВАНИЕ И super()
# =============================================================================

class A:
    def __init__(self):
        print("A.__init__")
        self.a = 1

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()  # Вызовет C.__init__ в ромбе, а не A.__init__!
        self.b = 2

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()
        self.c = 3

class D(B, C):
    """Ромбовидное наследование: D → B, C → A."""
    def __init__(self):
        print("D.__init__")
        super().__init__()  # Вызовет B.__init__ (по MRO)
        self.d = 4


def diamond_inheritance_demo():
    """Демонстрация ромбовидного наследования и cooperative super()."""
    print("\n" + "=" * 60)
    print("4. РОМБОВИДНОЕ НАСЛЕДОВАНИЕ")
    print("=" * 60)

    print(f"D MRO: {[c.__name__ for c in D.__mro__]}")
    # D → B → C → A → object

    d = D()
    print(f"Атрибуты: a={d.a}, b={d.b}, c={d.c}, d={d.d}")


# =============================================================================
# 5. ПРАКТИЧЕСКИЙ ПРИМЕР: ПЛАТЁЖНАЯ СИСТЕМА
# =============================================================================

class PaymentMethod(ABC):
    """Абстрактный платёжный метод."""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        ...

    @abstractmethod
    def get_info(self) -> str:
        ...


class CreditCard(PaymentMethod):
    def __init__(self, card_number: str, limit: float):
        self.card_number = card_number
        self.limit = limit
        self._spent = 0.0

    def pay(self, amount: float) -> bool:
        if self._spent + amount > self.limit:
            print(f"[!] Кредитный лимит превышен: {self._spent + amount:.2f} > {self.limit:.2f}")
            return False
        self._spent += amount
        print(f"[✓] Оплата {amount:.2f} ₽ картой {self.card_number[-4:]}")
        return True

    def get_info(self) -> str:
        return f"Карта ****{self.card_number[-4:]}, лимит: {self.limit:.2f} ₽, потрачено: {self._spent:.2f} ₽"


class PayPal(PaymentMethod):
    def __init__(self, email: str, balance: float):
        self.email = email
        self.balance = balance

    def pay(self, amount: float) -> bool:
        if amount > self.balance:
            print(f"[!] Недостаточно средств: {amount:.2f} > {self.balance:.2f}")
            return False
        self.balance -= amount
        print(f"[✓] Оплата {amount:.2f} ₽ через PayPal ({self.email})")
        return True

    def get_info(self) -> str:
        return f"PayPal: {self.email}, баланс: {self.balance:.2f} ₽"


class CryptoWallet(PaymentMethod):
    def __init__(self, wallet_address: str, balance_btc: float):
        self.wallet_address = wallet_address
        self.balance_btc = balance_btc

    def pay(self, amount: float) -> bool:
        price_per_btc = 5_000_000  # Курс для примера
        btc_needed = amount / price_per_btc
        if btc_needed > self.balance_btc:
            print(f"[!] Недостаточно BTC: нужно {btc_needed:.8f}, есть {self.balance_btc:.8f}")
            return False
        self.balance_btc -= btc_needed
        print(f"[✓] Оплата {btc_needed:.8f} BTC ({amount:.2f} ₽) с кошелька {self.wallet_address[:8]}...")
        return True

    def get_info(self) -> str:
        return f"Crypto: {self.wallet_address[:8]}..., баланс: {self.balance_btc:.8f} BTC"


def payment_system_demo():
    """Практический пример: платёжная система."""
    print("\n" + "=" * 60)
    print("5. ПРАКТИЧЕСКИЙ ПРИМЕР: ПЛАТЁЖНАЯ СИСТЕМА")
    print("=" * 60)

    # Полиморфизм: любой PaymentMethod можно использовать одинаково
    methods: list[PaymentMethod] = [
        CreditCard("1234-5678-9012-3456", limit=50000),
        PayPal("alice@example.com", balance=30000),
        CryptoWallet("1A1zP1...abc123", balance_btc=0.1),
    ]

    for method in methods:
        print(f"\n{method.get_info()}")
        method.pay(10000)
        method.pay(100000)  # Превышение лимита/баланса
        print(f"  После: {method.get_info()}")


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    simple_inheritance_demo()
    multiple_inheritance_demo()
    abstract_class_demo()
    diamond_inheritance_demo()
    payment_system_demo()

    print("\n" + "=" * 60)
    print("✅ УРОК 16 ЗАВЕРШЁН: НАСЛЕДОВАНИЕ ОСВОЕНО!")
    print("=" * 60)
