"""
test_parametrize.py — Параметризация тестов

Показывает:
- @pytest.mark.parametrize — один тест, много входных данных
- Параметризация с несколькими аргументами
- Комбинирование параметров
- ids для читаемых имён тестов
- Параметризация класса
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
from calculator import Calculator


# ============================================================
# ПРОСТАЯ ПАРАМЕТРИЗАЦИЯ
# ============================================================

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
    (-5, -3, -8),
    (0, 0, 0),
    (100, 200, 300),
    (1.5, 2.5, 4.0),
])
def test_add_parametrized(a, b, expected):
    """
    Один тест, 7 наборов данных!
    Pytest запустит test_add_parametrized[a-b-expected] для каждого.
    """
    calc = Calculator()
    assert calc.add(a, b) == expected


# ============================================================
# ПАРАМЕТРИЗАЦИЯ С IDS (ЧИТАЕМЫЕ ИМЕНА)
# ============================================================

@pytest.mark.parametrize("a,b,expected", [
    pytest.param(2, 3, 5, id="положительные"),
    pytest.param(-1, -1, -2, id="отрицательные"),
    pytest.param(0, 5, 5, id="с нулём"),
    pytest.param(1000, 2000, 3000, id="большие числа"),
])
def test_add_with_ids(a, b, expected):
    """Параметризация с читаемыми именами тестов."""
    calc = Calculator()
    assert calc.add(a, b) == expected


# ============================================================
# ПАРАМЕТРИЗАЦИЯ РАЗНЫХ ОПЕРАЦИЙ
# ============================================================

@pytest.mark.parametrize("operation,a,b,expected", [
    ("add", 2, 3, 5),
    ("add", -1, 1, 0),
    ("subtract", 10, 4, 6),
    ("subtract", 0, 5, -5),
    ("multiply", 3, 4, 12),
    ("multiply", -2, 5, -10),
    ("divide", 10, 2, 5),
    ("divide", 7, 2, 3.5),
])
def test_all_operations(operation, a, b, expected):
    """
    Один тест для всех операций!
    Используем getattr для динамического вызова метода.
    """
    calc = Calculator()
    method = getattr(calc, operation)
    result = method(a, b)
    assert result == expected


# ============================================================
# ПАРАМЕТРИЗАЦИЯ КЛАССА
# ============================================================

class TestParametrizedClass:
    """Параметризация применяется ко всем методам класса."""

    @pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
    def test_add_to_calculator(self, calculator, value):
        """Добавление разных чисел на чистый калькулятор."""
        calculator.add(value)
        assert calculator.value == value

    @pytest.mark.parametrize("a,expected_sign", [
        (1, "положительное"),
        (-1, "отрицательное"),
        (0, "ноль"),
    ])
    def test_sign(self, calculator, a, expected_sign):
        """Проверка знака числа."""
        calculator.add(a)
        if expected_sign == "положительное":
            assert calculator.is_positive()
        else:
            assert not calculator.is_positive()


# ============================================================
# КОМБИНИРОВАНИЕ ПАРАМЕТРОВ
# ============================================================

@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_cartesian_product(x, y):
    """
    Две параметризации = декартово произведение!
    3 × 2 = 6 тестов: (1,10) (1,20) (2,10) (2,20) (3,10) (3,20)
    """
    calc = Calculator()
    result = calc.add(x, y)
    print(f"  {x} + {y} = {result}")
    assert result == x + y
