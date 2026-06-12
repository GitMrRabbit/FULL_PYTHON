# 🧬 Урок 16: ООП — Наследование и Полиморфизм

## 📖 Теория

**Наследование** — механизм создания нового класса на основе существующего. **Полиморфизм** — способность объектов с одинаковым интерфейсом иметь разную реализацию.

---

## 🔹 Простое наследование

```python
class Animal:                          # Родитель (суперкласс)
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):                     # Наследник (подкласс)
    def __init__(self, name, breed):
        super().__init__(name)         # Вызов родительского __init__
        self.breed = breed

    def speak(self):                   # Переопределение (override)
        return "Гав!"
```

---

## 🔹 `super()` — доступ к родителю

```python
class Child(Parent):
    def __init__(self, x, y):
        super().__init__(x)     # Вызов метода родителя
        self.y = y

    def method(self):
        result = super().method()  # Результат родительского метода
        return f"Child({result})"
```

---

## 🔹 Множественное наследование

```python
class Duck(Animal, Flyable, Swimmable):
    """Наследует от Animal, Flyable и Swimmable."""
    pass
```

**MRO (Method Resolution Order)** — порядок поиска методов:
```
Duck → Animal → Flyable → Swimmable → object
```

Просмотр MRO:
```python
print(Duck.__mro__)
print(Duck.mro())
```

**Алгоритм C3-линеаризации** гарантирует:
- Дети раньше родителей
- Родители в порядке объявления
- Нет дублирования

---

## 🔹 Абстрактные классы (`abc`)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """Должен быть реализован наследниками."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

class Circle(Shape):
    def area(self): return 3.14 * self.r ** 2
    def perimeter(self): return 2 * 3.14 * self.r

# shape = Shape()  # TypeError! Нельзя создать абстрактный класс
```

---

## 🔹 Полиморфизм

```python
def print_area(shapes: list[Shape]):
    for shape in shapes:
        print(f"{shape.__class__.__name__}: {shape.area():.2f}")
        # Неважно, Circle это или Rectangle — метод area() есть у всех!

print_area([Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)])
```

**Duck Typing** (утиная типизация):
> «Если что-то выглядит как утка и крякает как утка — это утка»

```python
def make_it_speak(animal):
    print(animal.speak())  # Не проверяем тип! Просто вызываем speak()

make_it_speak(Dog("Рекс"))     # "Гав!"
make_it_speak(Cat("Мурка"))    # "Мяу!"
```

---

## 🔹 `isinstance()` / `issubclass()`

```python
isinstance(rex, Dog)      # True
isinstance(rex, Animal)   # True (Dog наследует Animal)
isinstance(rex, Cat)      # False

issubclass(Dog, Animal)   # True
issubclass(Dog, Cat)      # False
issubclass(Dog, object)   # True (всё наследует object)
```

---

## ⚠️ Проблемы множественного наследования

### Ромбовидное наследование (Diamond Problem)
```
   A
  / \
 B   C
  \ /
   D
```
Python решает через MRO (C3-линеаризация) + cooperative `super()`.

---

## 💡 Лучшие практики

1. **Предпочитайте композицию наследованию** — "has-a" вместо "is-a"
2. **Mixin-классы** — добавляют поведение, не предназначены для создания экземпляров
3. **`super()` всегда** — для cooperative множественного наследования
4. **Абстрактные классы** — для определения интерфейсов
5. **Не злоупотребляйте множественным наследованием** — усложняет понимание

---

## 🧪 Упражнения

1. Создайте иерархию классов Транспорт: Vehicle → Car, Motorcycle, Bicycle
2. Реализуйте систему логирования с абстрактным Logger и конкретными FileLogger, ConsoleLogger
3. Используя mixin'ы, добавьте JSON-сериализацию и сравнение к классам
4. Реализуйте паттерн "Фабрика" для создания разных типов платёжных методов
