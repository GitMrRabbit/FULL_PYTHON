"""
conftest.py — Фикстуры для уровня 02 (WebDriver + Page Objects)

Демонстрирует:
- Фикстуру driver с yield (setup + teardown)
- Фикстуры для Page Objects
- Скриншот при падении теста (через хук)
"""

import pytest
import sys
import os

# Добавляем путь к модулям уровня
sys.path.insert(0, os.path.dirname(__file__))

from utils.driver_factory import DriverFactory
from config.config_manager import config


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура WebDriver.
    
    Создаёт драйвер перед тестом и закрывает после.
    scope='function' — новый браузер для каждого теста.
    """
    browser = config.browser
    headless = config.headless
    
    print(f"\n  [Driver] Создаю {browser} драйвер (headless={headless})")
    driver_instance = DriverFactory.create_driver(browser, headless)
    
    yield driver_instance
    
    print(f"\n  [Driver] Закрываю драйвер")
    driver_instance.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """
    Фикстура: страница логина.
    
    Открывает страницу логина перед тестом.
    """
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.open()
    return page


# ============================================================
# ХУКИ PYTEST
# ============================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук: делает скриншот при падении теста.
    
    Скриншот сохраняется в директорию screenshots/ с именем теста.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            
            test_name = item.name
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
            
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\n  📸 Скриншот сохранён: {screenshot_path}")
            except Exception as e:
                print(f"\n  ⚠️ Не удалось сделать скриншот: {e}")
