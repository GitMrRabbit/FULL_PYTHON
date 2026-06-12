"""
login_page.py — Page Object для страницы логина (SauceDemo).

Демонстрирует:
- Конкретный Page Object, наследующий BasePage
- Локаторы как атрибуты класса
- Методы, соответствующие действиям пользователя
- Возврат других Page Object'ов при навигации
"""

from .base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object для страницы логина.
    
    Инкапсулирует:
    - Локаторы элементов страницы
    - Действия: ввод логина, пароля, клик по кнопке
    - Проверки: сообщения об ошибках
    """
    
    # === Локаторы ===
    USERNAME_INPUT = "id=user-name"
    PASSWORD_INPUT = "id=password"
    LOGIN_BUTTON = "id=login-button"
    ERROR_MESSAGE = "css=[data-test='error']"
    ERROR_BUTTON = "css=.error-button"
    
    # === Действия ===
    
    def open(self):
        """Открыть страницу логина."""
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    def enter_username(self, username):
        """Ввести имя пользователя."""
        self.fill(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password):
        """Ввести пароль."""
        self.fill(self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self):
        """Нажать кнопку Login."""
        self.click(self.LOGIN_BUTTON)
        # После успешного логина возвращаем страницу инвентаря
        from .inventory_page import InventoryPage
        return InventoryPage(self.driver, self.timeout)
    
    def login_as(self, username, password):
        """
        Полный сценарий логина.
        
        Возвращает InventoryPage при успехе.
        """
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login()
    
    # === Проверки ===
    
    def get_error_message(self):
        """Получить текст ошибки (если есть)."""
        if self.is_displayed(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_error_displayed(self):
        """Проверить, отображается ли сообщение об ошибке."""
        return self.is_displayed(self.ERROR_MESSAGE, timeout=2)
    
    def is_login_button_displayed(self):
        """Проверить, видна ли кнопка логина."""
        return self.is_displayed(self.LOGIN_BUTTON)
