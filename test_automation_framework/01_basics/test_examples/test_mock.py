"""
test_mock.py — Основы мокирования (unittest.mock)

Показывает:
- Mock — объект-заглушка
- MagicMock — Mock с магическими методами
- patch — временная подмена объектов
- side_effect — эмуляция исключений и побочных эффектов
- assert_called_with — проверка вызовов
"""

from unittest.mock import Mock, MagicMock, patch, PropertyMock
import pytest


# ============================================================
# БАЗОВЫЙ Mock
# ============================================================

def test_basic_mock():
    """Mock — объект, который можно настроить и проверить."""
    # Создаём мок
    mock_func = Mock(return_value=42)
    
    # Вызываем
    result = mock_func("hello", key="value")
    
    # Проверяем
    assert result == 42
    mock_func.assert_called_once_with("hello", key="value")


def test_mock_with_side_effect():
    """side_effect — разные возвращаемые значения при последовательных вызовах."""
    mock_func = Mock(side_effect=[1, 2, 3])
    
    assert mock_func() == 1
    assert mock_func() == 2
    assert mock_func() == 3
    
    with pytest.raises(StopIteration):
        mock_func()  # Значения кончились!


def test_mock_exception():
    """side_effect с исключением."""
    mock_func = Mock(side_effect=ValueError("Что-то пошло не так"))
    
    with pytest.raises(ValueError, match="Что-то пошло не так"):
        mock_func()


# ============================================================
# MagicMock — Mock с магическими методами
# ============================================================

def test_magic_mock():
    """MagicMock поддерживает магические методы."""
    mock_obj = MagicMock()
    
    # Можно использовать как контейнер
    mock_obj.__len__.return_value = 5
    assert len(mock_obj) == 5
    
    # Можно итерироваться
    mock_obj.__iter__.return_value = iter([1, 2, 3])
    assert list(mock_obj) == [1, 2, 3]
    
    # Можно использовать как контекстный менеджер
    mock_obj.__enter__.return_value = "resource"
    mock_obj.__exit__.return_value = False


# ============================================================
# PATCH — ВРЕМЕННАЯ ПОДМЕНА
# ============================================================

# Представьте, что это функция, делающая HTTP-запрос
def fetch_data_from_api(url):
    """
    Реальная функция, которая делает HTTP-запрос.
    Мы НЕ хотим делать реальные запросы в тестах!
    """
    import requests  # В реальном коде
    # response = requests.get(url)
    # return response.json()
    return {"data": "real"}  # Заглушка для примера


def test_patch_decorator():
    """
    @patch подменяет объект на время теста.
    После теста оригинал восстанавливается.
    """
    with patch(__name__ + '.fetch_data_from_api') as mock_fetch:
        # Настраиваем мок
        mock_fetch.return_value = {"data": "mocked!"}
        
        # Вызываем "реальную" функцию
        result = fetch_data_from_api("https://api.example.com")
        
        # Проверяем
        assert result == {"data": "mocked!"}
        mock_fetch.assert_called_once_with("https://api.example.com")


# ============================================================
# ПРИМЕР: ТЕСТИРОВАНИЕ СЕРВИСА С ВНЕШНЕЙ ЗАВИСИМОСТЬЮ
# ============================================================

class EmailService:
    """Сервис отправки email (внешняя зависимость)."""
    def send(self, to, subject, body):
        """Реальная отправка email."""
        pass  # В реальности: SMTP-соединение, отправка


class UserNotifier:
    """Бизнес-логика: уведомление пользователя."""
    def __init__(self, email_service):
        self.email_service = email_service
    
    def notify_user_created(self, user_email, user_name):
        """Отправляет приветственное письмо."""
        subject = f"Добро пожаловать, {user_name}!"
        body = f"Спасибо за регистрацию, {user_name}!"
        self.email_service.send(user_email, subject, body)
        return True


def test_user_notifier_with_mock():
    """
    Тестируем UserNotifier, НЕ отправляя реальных писем!
    """
    # Создаём мок для EmailService
    mock_email = Mock()
    
    # Создаём тестируемый объект с моком
    notifier = UserNotifier(mock_email)
    
    # Действие
    result = notifier.notify_user_created("anna@example.com", "Анна")
    
    # Проверки
    assert result is True
    
    # Проверяем, что send был вызван с правильными аргументами
    mock_email.send.assert_called_once_with(
        "anna@example.com",
        "Добро пожаловать, Анна!",
        "Спасибо за регистрацию, Анна!"
    )


# ============================================================
# ПРОВЕРКА МНОЖЕСТВЕННЫХ ВЫЗОВОВ
# ============================================================

def test_multiple_calls():
    """Проверка множественных вызовов mock-объекта."""
    mock = Mock()
    
    mock("first")
    mock("second")
    mock("third")
    
    # Сколько раз вызван?
    assert mock.call_count == 3
    
    # Проверка всех вызовов
    mock.assert_any_call("first")
    mock.assert_any_call("second")
    mock.assert_any_call("third")
    
    # Все вызовы (список)
    assert mock.call_args_list == [
        (("first",), {}),
        (("second",), {}),
        (("third",), {}),
    ]
