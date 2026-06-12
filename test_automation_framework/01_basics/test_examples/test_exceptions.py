"""
test_exceptions.py — Проверка исключений (pytest.raises)

Показывает:
- pytest.raises — проверка, что код вызывает исключение
- Проверка сообщения исключения (match)
- Проверка типа исключения
- Проверка нескольких исключений
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
from calculator import Calculator


# ============================================================
# БАЗОВАЯ ПРОВЕРКА ИСКЛЮЧЕНИЯ
# ============================================================

def test_division_by_zero():
    """Проверка, что деление на ноль вызывает ValueError."""
    calc = Calculator()
    
    with pytest.raises(ValueError):
        calc.divide(10, 0)


def test_division_by_zero_message():
    """Проверка ТИПА и СООБЩЕНИЯ исключения."""
    calc = Calculator()
    
    with pytest.raises(ValueError, match="Деление на ноль!"):
        calc.divide(10, 0)


def test_division_by_zero_variant():
    """Другой вариант: деление текущего значения на 0."""
    calc = Calculator()
    calc.add(10)  # value = 10
    
    with pytest.raises(ValueError):
        calc.divide(0)  # 10 / 0


# ============================================================
# ПРОВЕРКА НЕСКОЛЬКИХ ИСКЛЮЧЕНИЙ
# ============================================================

def test_multiple_exceptions():
    """Одна и та же операция может вызывать разные исключения."""
    calc = Calculator()
    
    # Деление на ноль — ValueError
    with pytest.raises(ValueError):
        calc.divide(10, 0)
    
    # А с обычными числами — без исключений
    result = calc.divide(10, 2)
    assert result == 5


# ============================================================
# ПАРАМЕТРИЗАЦИЯ С ИСКЛЮЧЕНИЯМИ
# ============================================================

@pytest.mark.parametrize("a,b,expected_exception", [
    (10, 0, ValueError),
    (0, 0, ValueError),
    (-5, 0, ValueError),
])
def test_division_errors_parametrized(a, b, expected_exception):
    """Параметризованная проверка исключений."""
    calc = Calculator()
    with pytest.raises(expected_exception):
        calc.divide(a, b)


# ============================================================
# ПРОВЕРКА КОРРЕКТНОСТИ ДАННЫХ ПОСЛЕ ИСКЛЮЧЕНИЯ
# ============================================================

def test_state_after_exception():
    """Проверка, что состояние не изменилось после исключения."""
    calc = Calculator()
    calc.add(42)  # value = 42
    history_before = len(calc.get_history())
    
    try:
        calc.divide(0)
    except ValueError:
        pass
    
    # Значение НЕ должно измениться после неудачной операции
    assert calc.value == 42
    # История тоже не должна измениться
    assert len(calc.get_history()) == history_before


# ============================================================
# СОБСТВЕННЫЕ ИСКЛЮЧЕНИЯ
# ============================================================

class NegativeNumberError(Exception):
    """Пользовательское исключение: отрицательное число."""
    pass


def square_root(value):
    """Возвращает квадратный корень (только для неотрицательных)."""
    if value < 0:
        raise NegativeNumberError(f"Нельзя извлечь корень из {value}")
    return value ** 0.5


def test_custom_exception():
    """Проверка пользовательского исключения."""
    with pytest.raises(NegativeNumberError, match="Нельзя извлечь корень из -4"):
        square_root(-4)


def test_custom_exception_not_raised():
    """Проверка, что исключение НЕ вызывается для корректных данных."""
    result = square_root(16)
    assert result == 4.0


# ============================================================
# FAIL — ПРИНУДИТЕЛЬНЫЙ ПРОВАЛ ТЕСТА
# ============================================================

def test_fail_example():
    """pytest.fail() — принудительно завалить тест."""
    condition = True
    if not condition:
        pytest.fail("Условие не выполнено!")
    assert condition
