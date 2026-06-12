"""
conftest.py — общие фикстуры для всех тестов уровня 01_basics.

Pytest автоматически обнаруживает conftest.py в директории тестов
и делает фикстуры доступными для всех тестовых файлов.
"""

import pytest
import sys
import os

# Добавляем путь к утилитам
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from calculator import Calculator


# ============================================================
# ФИКСТУРЫ
# ============================================================

@pytest.fixture
def calculator():
    """
    Базовая фикстура: создаёт новый экземпляр Calculator
    для каждого теста.
    
    scope по умолчанию = 'function' (для каждой тестовой функции)
    """
    return Calculator()


@pytest.fixture
def calculator_with_value():
    """
    Фикстура, возвращающая калькулятор с начальным значением 100.
    """
    return Calculator(initial_value=100)


@pytest.fixture(scope="module")
def module_calculator():
    """
    Фикстура с scope='module': создаётся ОДИН раз на весь модуль.
    Полезно для дорогих операций (БД, файлы, WebDriver).
    """
    print("\n  [module_calculator] Создаю калькулятор для модуля")
    calc = Calculator()
    yield calc
    print("\n  [module_calculator] Завершаю работу (teardown модуля)")


@pytest.fixture(scope="session")
def session_config():
    """
    Фикстура с scope='session': создаётся ОДИН раз на всю сессию тестов.
    Идеально для конфигурации, подключения к БД и т.д.
    """
    config = {
        "base_url": "https://example.com",
        "timeout": 30,
        "environment": "test"
    }
    return config
