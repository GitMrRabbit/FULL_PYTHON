"""
Класс Calculator — объект для тестирования.

Используется во всех примерах уровня 01_basics.
Содержит базовые арифметические операции и несколько
специальных методов для демонстрации разных типов тестов.
"""


class Calculator:
    """Простой калькулятор с базовыми операциями."""

    def __init__(self, initial_value=0):
        """Инициализация с начальным значением."""
        self.value = initial_value
        self.history = []  # История операций

    def add(self, a, b=None):
        """Сложение. Если b не указано — прибавляет к текущему значению."""
        if b is None:
            result = self.value + a
            self.value = result
        else:
            result = a + b
        self.history.append(f"add({a}, {b}) = {result}")
        return result

    def subtract(self, a, b=None):
        """Вычитание."""
        if b is None:
            result = self.value - a
            self.value = result
        else:
            result = a - b
        self.history.append(f"subtract({a}, {b}) = {result}")
        return result

    def multiply(self, a, b=None):
        """Умножение."""
        if b is None:
            result = self.value * a
            self.value = result
        else:
            result = a * b
        self.history.append(f"multiply({a}, {b}) = {result}")
        return result

    def divide(self, a, b=None):
        """Деление. Возбуждает ValueError при делении на 0."""
        if b is None:
            if a == 0:
                raise ValueError("Деление на ноль!")
            result = self.value / a
            self.value = result
        else:
            if b == 0:
                raise ValueError("Деление на ноль!")
            result = a / b
        self.history.append(f"divide({a}, {b}) = {result}")
        return result

    def reset(self):
        """Сброс калькулятора."""
        self.value = 0
        self.history.clear()
        return self.value

    def get_history(self):
        """Возвращает историю операций."""
        return self.history.copy()

    def is_positive(self):
        """Проверяет, положительное ли текущее значение."""
        return self.value > 0

    def power(self, exponent):
        """Возведение текущего значения в степень."""
        result = self.value ** exponent
        self.history.append(f"power({exponent}) = {result}")
        self.value = result
        return result

    def __str__(self):
        return f"Calculator(value={self.value})"

    def __repr__(self):
        return self.__str__()
