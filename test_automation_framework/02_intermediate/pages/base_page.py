"""
base_page.py — Базовый класс страницы (Page Object Model)

Демонстрирует:
- POM паттерн: каждая страница — отдельный класс
- Локаторы элементов
- Базовые действия: click, fill, get_text
- Ожидания (wait)
- Общие методы для всех страниц
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """
    Базовый класс для всех Page Object'ов.
    
    Содержит общие методы работы с WebDriver:
    - Поиск элементов
    - Клики, ввод текста
    - Ожидания
    - Скроллы
    """
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    # === Поиск элементов ===
    
    def find_element(self, locator):
        """Найти ОДИН элемент. Ждёт появления в DOM."""
        by, value = self._parse_locator(locator)
        return self.wait.until(
            EC.presence_of_element_located((by, value))
        )
    
    def find_elements(self, locator):
        """Найти ВСЕ элементы, соответствующие локатору."""
        by, value = self._parse_locator(locator)
        return self.driver.find_elements(by, value)
    
    def find_clickable(self, locator):
        """Найти кликабельный элемент (ждёт кликабельности)."""
        by, value = self._parse_locator(locator)
        return self.wait.until(
            EC.element_to_be_clickable((by, value))
        )
    
    def find_visible(self, locator):
        """Найти видимый элемент."""
        by, value = self._parse_locator(locator)
        return self.wait.until(
            EC.visibility_of_element_located((by, value))
        )
    
    # === Действия с элементами ===
    
    def click(self, locator):
        """Клик по элементу."""
        element = self.find_clickable(locator)
        element.click()
        return self
    
    def fill(self, locator, text):
        """Ввести текст в поле (с предварительной очисткой)."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return self
    
    def get_text(self, locator):
        """Получить текст элемента."""
        element = self.find_visible(locator)
        return element.text
    
    def get_attribute(self, locator, attribute):
        """Получить значение атрибута элемента."""
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    # === Проверки ===
    
    def is_displayed(self, locator, timeout=None):
        """Проверить, отображается ли элемент."""
        try:
            by, value = self._parse_locator(locator)
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_element_present(self, locator):
        """Проверить наличие элемента в DOM (может быть скрыт)."""
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False
    
    # === Навигация ===
    
    def open(self, url):
        """Открыть URL."""
        self.driver.get(url)
        return self
    
    def refresh(self):
        """Обновить страницу."""
        self.driver.refresh()
        return self
    
    def get_current_url(self):
        """Получить текущий URL."""
        return self.driver.current_url
    
    def get_title(self):
        """Получить заголовок страницы."""
        return self.driver.title
    
    # === Скролл ===
    
    def scroll_to(self, locator):
        """Прокрутить страницу до элемента."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return self
    
    # === Вспомогательные методы ===
    
    def _parse_locator(self, locator):
        """
        Парсит локатор в формате (By.XXX, "value") или строку "css|.class".
        
        Поддерживаемые форматы:
        - (By.ID, "my_id")
        - (By.XPATH, "//div")
        - "id=my_id"
        - "css=.my_class"
        - "xpath=//div"
        """
        if isinstance(locator, tuple):
            return locator
        
        if isinstance(locator, str):
            if locator.startswith("id="):
                return By.ID, locator[3:]
            elif locator.startswith("css="):
                return By.CSS_SELECTOR, locator[4:]
            elif locator.startswith("xpath="):
                return By.XPATH, locator[6:]
            elif locator.startswith("name="):
                return By.NAME, locator[5:]
            elif locator.startswith("class="):
                return By.CLASS_NAME, locator[6:]
            elif locator.startswith("tag="):
                return By.TAG_NAME, locator[4:]
            else:
                # По умолчанию — CSS селектор
                return By.CSS_SELECTOR, locator
        
        raise ValueError(f"Неподдерживаемый формат локатора: {locator}")
