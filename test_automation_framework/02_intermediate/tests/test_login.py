"""
test_login.py — Тесты логина с использованием Page Object Model

Демонстрирует:
- Тесты, использующие Page Object и DTO
- Параметризованные тесты с DTO
- Позитивные и негативные сценарии
- Проверки с использованием методов Page Object
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dto.user_dto import UserDTO, STANDARD_USER, LOCKED_OUT_USER
from pages.login_page import LoginPage


@pytest.mark.smoke
class TestLogin:
    """Группа тестов для проверки логина."""
    
    def test_successful_login(self, driver):
        """
        Позитивный сценарий: успешный вход с валидными данными.
        
        Использует стандартного пользователя (DTO).
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        # Используем DTO для данных
        inventory_page = login_page.login_as(
            STANDARD_USER.username,
            STANDARD_USER.password
        )
        
        # Проверяем успешный вход: URL изменился
        assert "inventory.html" in driver.current_url, \
            f"Не удалось войти! Текущий URL: {driver.current_url}"
    
    def test_login_with_invalid_password(self, driver):
        """
        Негативный сценарий: вход с неверным паролем.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        login_page.enter_username(STANDARD_USER.username)
        login_page.enter_password("wrong_password")
        login_page.click_login()
        
        # Проверяем сообщение об ошибке
        assert login_page.is_error_displayed(), "Сообщение об ошибке не отображается!"
        error_text = login_page.get_error_message()
        assert "Username and password do not match" in error_text, \
            f"Неверный текст ошибки: {error_text}"
    
    def test_login_locked_out_user(self, driver):
        """
        Негативный сценарий: заблокированный пользователь.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        login_page.login_as(
            LOCKED_OUT_USER.username,
            LOCKED_OUT_USER.password
        )
        
        assert login_page.is_error_displayed()
        error_text = login_page.get_error_message()
        assert "locked out" in error_text.lower(), \
            f"Неверный текст ошибки: {error_text}"
    
    def test_login_empty_credentials(self, driver):
        """Негативный сценарий: пустые поля."""
        login_page = LoginPage(driver)
        login_page.open()
        
        # Пустые логин и пароль
        login_page.click_login()
        
        assert login_page.is_error_displayed()
        error_text = login_page.get_error_message()
        assert "Username is required" in error_text, \
            f"Неверный текст ошибки: {error_text}"


@pytest.mark.parametrize("user", [
    STANDARD_USER,
    # Можно добавить других пользователей
])
def test_login_with_dto(driver, user):
    """
    Параметризованный тест: вход с разными DTO.
    
    Демонстрирует гибкость DTO + параметризации.
    """
    login_page = LoginPage(driver)
    login_page.open()
    
    login_page.login_as(user.username, user.password)
    
    if user.is_locked:
        assert login_page.is_error_displayed()
    else:
        assert "inventory.html" in driver.current_url
