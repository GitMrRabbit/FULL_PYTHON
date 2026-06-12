# 🧪 Урок 27: Основы тестирования

## 📖 Виды тестирования

| Тип | Что проверяет | Инструменты |
|-----|--------------|-------------|
| Unit | Отдельные функции/классы | unittest, pytest |
| Integration | Взаимодействие компонентов | pytest + фикстуры |
| E2E | Сценарии целиком | Selenium, Playwright |

---

## 🔹 unittest

```python
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(1, 0)
```

---

## 🔹 pytest (рекомендуемый)

```python
import pytest

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    assert calculator.add(2, 3) == 5

@pytest.mark.parametrize("a,b,expected", [(1,2,3), (0,0,0)])
def test_param(calculator, a, b, expected):
    assert calculator.add(a, b) == expected

with pytest.raises(ValueError, match=".*"):
    raise ValueError("bad value")
```

---

## 🔹 Mock

```python
from unittest.mock import Mock, patch

mock = Mock(return_value=42)
mock()  # 42

mock_api = Mock()
mock_api.get.return_value = {"name": "Анна"}
service = UserService(mock_api)
name = service.get_user_name(1)  # "Анна"
mock_api.get.assert_called_once_with("/users/1")
```

---

## 🔹 Coverage

```bash
pip install pytest-cov
pytest --cov=src --cov-report=html --cov-fail-under=80
```

---

## 🧪 Упражнения

1. Напишите тесты для класса Calculator
2. Используйте параметризацию для граничных значений
3. Замокируйте внешний API-клиент
4. Настройте coverage и добейтесь 90%+ покрытия
