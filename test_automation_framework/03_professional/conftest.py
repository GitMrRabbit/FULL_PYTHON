"""Глобальные фикстуры и хуки для профессионального фреймворка."""

import pytest
import logging
from pathlib import Path
from datetime import datetime

# Импорт только если модули существуют
try:
    from common.logger import setup_logger
    logger = setup_logger("test_framework")
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("test_framework")


def pytest_configure(config):
    """Регистрация кастомных маркеров."""
    config.addinivalue_line("markers", "smoke: Критические тесты")
    config.addinivalue_line("markers", "regression: Регрессионные тесты")
    config.addinivalue_line("markers", "e2e: End-to-end тесты")
    config.addinivalue_line("markers", "api: API тесты")
    config.addinivalue_line("markers", "web: Web/UI тесты")
    config.addinivalue_line("markers", "slow: Медленные тесты")
    config.addinivalue_line("markers", "db: Тесты с БД")


@pytest.fixture(scope="session")
def test_config():
    """Загрузка конфигурации для всей сессии."""
    return {
        "base_url": "https://jsonplaceholder.typicode.com",
        "timeout": 30,
        "retries": 3,
    }


@pytest.fixture(scope="function")
def test_id(request):
    """Уникальный ID теста для логирования."""
    return f"{request.node.name}_{datetime.now().strftime('%H%M%S')}"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении UI-тестов."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            try:
                screenshot_dir = Path("reports/screenshots")
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                filename = f"{item.name}_{datetime.now():%Y%m%d_%H%M%S}.png"
                driver.save_screenshot(str(screenshot_dir / filename))
                logger.error(f"Скриншот сохранён: {filename}")
            except Exception as e:
                logger.warning(f"Не удалось сохранить скриншот: {e}")


@pytest.fixture(scope="session", autouse=True)
def global_setup():
    """Глобальная инициализация перед всеми тестами."""
    logger.info("=" * 50)
    logger.info("ЗАПУСК ТЕСТОВОГО ФРЕЙМВОРКА")
    logger.info("=" * 50)
    yield
    logger.info("=" * 50)
    logger.info("ТЕСТОВЫЙ ПРОГОН ЗАВЕРШЁН")
    logger.info("=" * 50)
