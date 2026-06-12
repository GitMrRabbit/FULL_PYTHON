"""
Урок 27: Основы тестирования (unittest + pytest)
=================================================

Темы:
  - Зачем нужно тестирование (виды, пирамида)
  - unittest: TestCase, assertEqual, setUp/tearDown
  - pytest: fixture, parametrize, markers, raises
  - Mock/MagicMock
  - Покрытие кода (coverage)
"""

import pytest
import unittest
from unittest.mock import Mock, MagicMock, patch, sentinel


# =============================================================================
# 1. ТЕСТИРУЕМЫЙ КОД
# =============================================================================

class Calculator:
    """Тестируемый класс (тот же, что в 01_basics/utils/calculator.py)."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Деление на ноль")
        return a / b

    def average(self, numbers: list[float]) -> float:
        if not numbers:
            raise ValueError("Список не может быть пустым")
        return sum(numbers) / len(numbers)


class UserService:
    """Сервис, зависящий от внешнего API (для демонстрации моков)."""

    def __init__(self, api_client):
        self.api = api_client

    def get_user_name(self, user_id: int) -> str:
        user = self.api.get(f"/users/{user_id}")
        return user["name"]

    def create_user(self, name: str, email: str) -> dict:
        return self.api.post("/users", {"name": name, "email": email})


# =============================================================================
# 2. UNITTEST
# =============================================================================

class TestCalculatorUnittest(unittest.TestCase):
    """unittest стиль тестирования."""

    def setUp(self):
        """Выполняется ПЕРЕД каждым тестом."""
        self.calc = Calculator()
        print(f"\n  setUp: создан Calculator")

    def tearDown(self):
        """Выполняется ПОСЛЕ каждого теста."""
        print(f"  tearDown: очистка")

    def test_add_positive(self):
        """Проверка сложения положительных чисел."""
        result = self.calc.add(3, 4)
        self.assertEqual(result, 7)

    def test_add_negative(self):
        """Проверка сложения отрицательных чисел."""
        self.assertEqual(self.calc.add(-3, -4), -7)
        self.assertEqual(self.calc.add(-3, 4), 1)

    def test_divide_normal(self):
        """Проверка обычного деления."""
        self.assertAlmostEqual(self.calc.divide(10, 3), 3.33333, places=4)

    def test_divide_by_zero(self):
        """Проверка деления на ноль (ожидаем исключение)."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_average_empty(self):
        """Проверка пустого списка."""
        with self.assertRaises(ValueError):
            self.calc.average([])

    def test_average(self):
        """Проверка среднего арифметического."""
        self.assertEqual(self.calc.average([2, 4, 6]), 4.0)

    @unittest.skip("Демонстрация skip")
    def test_skip_example(self):
        pass

    @unittest.skipIf(True, "Условный skip")
    def test_skipif_example(self):
        pass


# =============================================================================
# 3. PYTEST
# =============================================================================

# Фикстура (fixture) — аналог setUp/tearDown, но мощнее
@pytest.fixture
def calculator():
    """Создаёт новый Calculator для каждого теста."""
    return Calculator()


@pytest.fixture
def sample_numbers():
    """Предоставляет тестовые данные."""
    return [1, 2, 3, 4, 5]


class TestCalculatorPytest:
    """pytest стиль (класс не обязателен, но можно)."""

    def test_add(self, calculator):
        """Фикстура передаётся как аргумент."""
        assert calculator.add(3, 4) == 7
        assert calculator.add(-1, 1) == 0
        assert calculator.add(0, 0) == 0

    def test_divide(self, calculator):
        assert calculator.divide(10, 2) == 5.0

    def test_divide_by_zero(self, calculator):
        with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
            calculator.divide(10, 0)

    def test_average(self, calculator, sample_numbers):
        assert calculator.average(sample_numbers) == 3.0

    def test_average_empty(self, calculator):
        with pytest.raises(ValueError, match="не может быть пустым"):
            calculator.average([])

    # Параметризация
    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
        (100, 200, 300),
    ])
    def test_add_parametrized(self, calculator, a, b, expected):
        assert calculator.add(a, b) == expected

    # Маркеры
    @pytest.mark.slow
    def test_slow_operation(self, calculator):
        import time
        time.sleep(0.1)
        assert calculator.add(1, 1) == 2

    @pytest.mark.skip(reason="Ещё не реализовано")
    def test_future_feature(self):
        pass

    @pytest.mark.xfail(reason="Известный баг")
    def test_known_bug(self, calculator):
        assert calculator.add(2, 2) == 5  # Намеренно падает


# =============================================================================
# 4. МОКИ (unittest.mock)
# =============================================================================

def test_mock_basics():
    """Демонстрация Mock и MagicMock."""

    # Простой Mock
    mock = Mock(return_value=42)
    assert mock() == 42
    assert mock(1, 2, key="value") == 42

    # Проверка вызовов
    mock.assert_called()            # Был вызван
    mock.assert_called_with(1, 2, key="value")  # Последний вызов с этими аргументами
    print(f"Количество вызовов: {mock.call_count}")
    print(f"Аргументы вызовов: {mock.call_args_list}")

    # side_effect — последовательные возвраты
    mock2 = Mock(side_effect=[1, 2, 3])
    assert mock2() == 1
    assert mock2() == 2
    assert mock2() == 3

    # side_effect — исключение
    mock3 = Mock(side_effect=ValueError("Ошибка!"))
    try:
        mock3()
    except ValueError as e:
        print(f"Исключение из mock: {e}")


def test_user_service_mock():
    """Тестирование с моками: изолируем API-клиент."""

    # Создаём мок API
    mock_api = Mock()
    mock_api.get.return_value = {"id": 1, "name": "Анна"}
    mock_api.post.return_value = {"id": 2, "name": "Борис", "email": "boris@example.com"}

    service = UserService(mock_api)

    # Тест get_user_name
    name = service.get_user_name(1)
    assert name == "Анна"
    mock_api.get.assert_called_once_with("/users/1")

    # Тест create_user
    user = service.create_user("Борис", "boris@example.com")
    assert user["id"] == 2
    mock_api.post.assert_called_once_with("/users", {"name": "Борис", "email": "boris@example.com"})


@patch("__main__.UserService")  # Не работает напрямую, пример синтаксиса
def test_with_patch_decorator():
    """
    @patch заменяет указанный объект на Mock.

    @patch("module.ClassName")
    def test_something(mock_class):
        mock_class.return_value.method.return_value = 42
        ...
    """
    pass


# =============================================================================
# 5. COVERAGE (ПОКРЫТИЕ КОДА)
# =============================================================================

COVERAGE_INFO = """
╔══════════════════════════════════════════════════════════════════╗
║  ПОКРЫТИЕ КОДА (COVERAGE)                                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  # Установка                                                     ║
║  pip install pytest-cov                                          ║
║                                                                  ║
║  # Запуск тестов с покрытием                                     ║
║  pytest --cov=my_package --cov-report=html                       ║
║                                                                  ║
║  # Отчёт в терминале                                             ║
║  pytest --cov=my_package --cov-report=term-missing               ║
║                                                                  ║
║  # Минимальный порог                                             ║
║  pytest --cov=my_package --cov-fail-under=80                     ║
║                                                                  ║
║  Виды покрытия:                                                  ║
║    - Покрытие строк (line coverage)                              ║
║    - Покрытие ветвлений (branch coverage)                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("УРОК 27: ОСНОВЫ ТЕСТИРОВАНИЯ")
    print("=" * 60)

    print("\nДля запуска тестов используйте:")
    print("  python -m pytest 27_testing_basics/testing_basics.py -v")
    print("  python -m pytest 27_testing_basics/testing_basics.py -v -k 'add'")
    print("  python -m pytest 27_testing_basics/testing_basics.py --cov=. --cov-report=term")

    print("\nДемонстрация моков:")
    test_mock_basics()
    test_user_service_mock()

    print(COVERAGE_INFO)

    print("=" * 60)
    print("✅ УРОК 27 ЗАВЕРШЁН: ТЕСТИРОВАНИЕ ОСВОЕНО!")
    print("=" * 60)
