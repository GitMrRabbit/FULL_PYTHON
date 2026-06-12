"""
driver_factory.py — Фабрика WebDriver'ов.

Демонстрирует:
- Создание WebDriver для разных браузеров (Chrome, Firefox)
- Настройка опций (headless, window size)
- Паттерн Factory Method
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class DriverFactory:
    """
    Фабрика для создания экземпляров WebDriver.
    
    Использование:
        driver = DriverFactory.create_driver('chrome', headless=True)
    """
    
    @staticmethod
    def create_driver(browser_name='chrome', headless=False):
        """
        Создать WebDriver для указанного браузера.
        
        Args:
            browser_name: 'chrome' или 'firefox'
            headless: запуск без GUI
            
        Returns:
            WebDriver instance
        """
        browser_name = browser_name.lower()
        
        if browser_name == 'chrome':
            return DriverFactory._create_chrome_driver(headless)
        elif browser_name == 'firefox':
            return DriverFactory._create_firefox_driver(headless)
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}")
    
    @staticmethod
    def _create_chrome_driver(headless=False):
        """Создать Chrome WebDriver."""
        options = ChromeOptions()
        
        if headless:
            options.add_argument('--headless=new')
        
        # Стандартные опции
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        
        # Отключаем автоматизацию (чтобы сайты не детектили)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless=False):
        """Создать Firefox WebDriver."""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        return driver


# Альтернатива: контекстный менеджер для WebDriver
class DriverContext:
    """
    Контекстный менеджер для автоматического закрытия драйвера.
    
    Использование:
        with DriverContext('chrome') as driver:
            driver.get('https://example.com')
    """
    
    def __init__(self, browser_name='chrome', headless=False):
        self.browser_name = browser_name
        self.headless = headless
        self.driver = None
    
    def __enter__(self):
        self.driver = DriverFactory.create_driver(self.browser_name, self.headless)
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
