"""
test_simple.py — Простейшие тесты с assert

Показывает:
- Базовые assert-проверки
- AAA Pattern (Arrange-Act-Assert)
- Разные типы assert (==, !=, is, in, isinstance, почти-равенство)
- Именование тестов: test_*
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
from calculator import Calculator


# ============================================================
# ПРОСТЕЙШИЕ ТЕСТЫ БЕЗ ФИКСТУР
# ============================================================

def test_addition():
    """Проверка сложения двух чисел."""
    # Arrange
    calc = Calculator()
    # Act
    result = calc.add(2, 3)
    # Assert
    assert result == 5
    assert isinstance(result, (int, float))


def test_subtraction():
    """Проверка вычитания."""
    calc = Calculator()
    assert calc.subtract(10, 4) == 6


def test_multiplication():
    """Проверка умножения."""
    calc = Calculator()
    assert calc.multiply(7, 3) == 21


def test_division():
    """Проверка деления."""
    calc = Calculator()
    assert calc.divide(10, 2) == 5


def test_division_float():
    """Проверка деления с дробным результатом."""
    calc = Calculator()
    assert calc.divide(7, 2) == 3.5


# ============================================================
# ТЕСТЫ С ФИКСТУРАМИ (из conftest.py)
# ============================================================

def test_with_fixture(calculator):
    """
    Фикстура calculator автоматически внедряется pytest'ом.
    """
    result = calculator.add(10, 20)
    assert result == 30


def test_calculator_is_fresh(calculator):
    """
    Каждый тест получает СВЕЖИЙ экземпляр калькулятора.
    Значение по умолчанию = 0.
    """
    assert calculator.value == 0


def test_calculator_with_initial_value(calculator_with_value):
    """Фикстура с начальным значением 100."""
    assert calculator_with_value.value == 100


# ============================================================
# РАЗНЫЕ ТИПЫ ASSERT
# ============================================================

class TestCalculatorAdvanced:
    """Группа тестов в классе (альтернатива отдельным функциям)."""

    def test_accumulate(self, calculator):
        """Последовательные операции с накоплением."""
        calculator.add(10)       # 0 + 10 = 10
        calculator.multiply(3)   # 10 * 3 = 30
        calculator.subtract(5)   # 30 - 5 = 25
        assert calculator.value == 25

    def test_reset(self, calculator):
        """Сброс обнуляет значение и историю."""
        calculator.add(42)
        assert calculator.value == 42
        calculator.reset()
        assert calculator.value == 0
        assert calculator.history == []

    def test_history(self, calculator):
        """Проверка записи истории."""
        calculator.add(1, 2)
        calculator.multiply(3, 4)
        history = calculator.get_history()
        assert len(history) == 2
        assert "add(1, 2) = 3" in history[0]
        assert "multiply(3, 4) = 12" in history[1]

    def test_is_positive(self, calculator):
        """Проверка метода is_positive()."""
        assert calculator.is_positive() is False  # 0 — не положительное
        calculator.add(1)
        assert calculator.is_positive() is True

    def test_power(self, calculator):
        """Возведение в степень."""
        calculator.add(2)  # value = 2
        result = calculator.power(3)  # 2^3 = 8
        assert result == 8
        assert calculator.value == 8


# ============================================================
# СПЕЦИАЛЬНЫЕ ASSERT-ПРОВЕРКИ
# ============================================================

def test_assert_types():
    """Разные assert в pytest."""
    # Равенство
    assert 2 + 2 == 4

    # Неравенство
    assert 2 + 2 != 5

    # True / False
    assert 5 > 3
    assert not (3 > 5)

    # is (идентичность)
    a = [1, 2]
    b = a
    assert a is b

    # is not
    c = [1, 2]
    assert a is not c

    # in (вхождение)
    assert 3 in [1, 2, 3]
    assert "e" in "hello"
    assert "name" in {"name": "Анна"}

    # not in
    assert 99 not in [1, 2, 3]

    # isinstance
    assert isinstance(42, int)
    assert isinstance("hello", str)

    # Почти-равенство (для float)
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 0.1 + 0.2 == pytest.approx(0.3, abs=0.001)  # абсолютная погрешность
    assert 0.1 + 0.2 == pytest.approx(0.3, rel=0.01)   # относительная погрешность

    # None
    result = None
    assert result is None
    assert result is not 42


def test_string_asserts():
    """Assert для строк."""
    text = "Hello, World!"

    assert text.startswith("Hello")
    assert text.endswith("!")
    assert "World" in text
    assert text.upper() == "HELLO, WORLD!"
    assert len(text) == 13


def test_list_asserts():
    """Assert для списков."""
    items = [1, 2, 3, 4, 5]

    assert len(items) == 5
    assert items[0] == 1
    assert items[-1] == 5
    assert sorted(items, reverse=True) == [5, 4, 3, 2, 1]


def test_dict_asserts():
    """Assert для словарей."""
    user = {"name": "Анна", "age": 25, "city": "Москва"}

    assert "name" in user
    assert user["age"] == 25
    assert user.get("country", "Россия") == "Россия"
    assert list(user.keys()) == ["name", "age", "city"]
