"""
Урок 29: Логирование в Python
==============================

Темы:
  - Модуль logging: уровни, handlers, formatters
  - Логирование в файл, консоль, несколько обработчиков
  - Фильтры и адаптеры
  - Структурное логирование (JSON)
  - Лучшие практики
"""

import logging
import logging.handlers
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Any


# =============================================================================
# 1. БАЗОВОЕ ЛОГИРОВАНИЕ
# =============================================================================

def basic_logging_demo():
    """Демонстрация базового логирования."""
    print("=" * 60)
    print("1. БАЗОВОЕ ЛОГИРОВАНИЕ")
    print("=" * 60)

    # Настройка базового конфига
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    logger = logging.getLogger(__name__)

    # Уровни логирования (по возрастанию важности)
    logger.debug("Детальная отладочная информация")    # Не выведется (INFO > DEBUG)
    logger.info("Информационное сообщение")
    logger.warning("Предупреждение!")
    logger.error("Ошибка!")
    logger.critical("Критическая ошибка!")

    # Уровни логирования
    print("\nУровни (порог срабатывания):")
    for level in [logging.DEBUG, logging.INFO, logging.WARNING,
                  logging.ERROR, logging.CRITICAL]:
        print(f"  {logging.getLevelName(level):8s} = {level}")


# =============================================================================
# 2. РАСШИРЕННАЯ НАСТРОЙКА
# =============================================================================

def setup_advanced_logger(log_dir: str = "logs") -> logging.Logger:
    """
    Создаёт логгер с записью в файл (с ротацией) и в консоль.
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("advanced")
    logger.setLevel(logging.DEBUG)

    # Форматтеры
    detailed_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_fmt = logging.Formatter(
        "[%(levelname)-8s] %(message)s"
    )

    # File handler (с ротацией по размеру: 1 МБ, 3 файла)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_fmt)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_fmt)
    logger.addHandler(console_handler)

    return logger


def advanced_logging_demo():
    """Демонстрация расширенного логирования."""
    print("\n" + "=" * 60)
    print("2. РАСШИРЕННОЕ ЛОГИРОВАНИЕ")
    print("=" * 60)

    logger = setup_advanced_logger()

    logger.debug("Детали: x=42, y=15")
    logger.info("Приложение запущено")
    logger.warning("Конфигурация не найдена, использую по умолчанию")

    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception("Ошибка при вычислении")  # exc_info=True автоматически

    print(f"[OK] Логи записаны в logs/app.log")


# =============================================================================
# 3. СТРУКТУРНОЕ ЛОГИРОВАНИЕ
# =============================================================================

class JsonFormatter(logging.Formatter):
    """Форматтер для вывода логов в JSON (для ELK, Splunk и т.д.)."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }

        # Дополнительные поля из extra
        for key in ("user_id", "request_id", "duration"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = str(record.exc_info[1])

        return json.dumps(log_entry, ensure_ascii=False)


def structured_logging_demo():
    """Демонстрация структурного (JSON) логирования."""
    print("\n" + "=" * 60)
    print("3. СТРУКТУРНОЕ ЛОГИРОВАНИЕ (JSON)")
    print("=" * 60)

    logger = logging.getLogger("json_logger")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    # Обычное сообщение
    logger.info("Пользователь вошёл в систему")

    # С дополнительными полями (через extra)
    logger.info(
        "Запрос обработан",
        extra={"user_id": 42, "request_id": "abc-123", "duration": 0.235}
    )

    # Ошибка
    try:
        raise ValueError("Некорректные данные")
    except ValueError:
        logger.error("Ошибка валидации", extra={"user_id": 42})

    print("[OK] JSON-логирование продемонстрировано")


# =============================================================================
# 4. ДЕКОРАТОР ДЛЯ ЛОГИРОВАНИЯ
# =============================================================================

def log_execution(logger: logging.Logger | None = None):
    """Декоратор: логирует вызов и результат функции."""
    if logger is None:
        logger = logging.getLogger(__name__)

    def decorator(func):
        import functools

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Вызов {func.__name__}(args={args}, kwargs={kwargs})")
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                logger.debug(f"{func.__name__} → {result!r} ({elapsed:.4f}с)")
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start
                logger.error(f"{func.__name__} ОШИБКА: {e} ({elapsed:.4f}с)")
                raise
        return wrapper
    return decorator


def decorator_logging_demo():
    """Демонстрация декоратора логирования."""
    print("\n" + "=" * 60)
    print("4. ДЕКОРАТОР ЛОГИРОВАНИЯ")
    print("=" * 60)

    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    logger = logging.getLogger("demo")

    @log_execution(logger)
    def calculate(a: int, b: int) -> int:
        return a * b + a + b

    @log_execution(logger)
    def fail_function():
        raise RuntimeError("Тестовая ошибка")

    print(f"calculate(3, 4) = {calculate(3, 4)}")
    try:
        fail_function()
    except RuntimeError:
        pass  # Перехвачено


# =============================================================================
# 5. ЛУЧШИЕ ПРАКТИКИ
# =============================================================================

BEST_PRACTICES = """
╔══════════════════════════════════════════════════════════════════╗
║  ЛУЧШИЕ ПРАКТИКИ ЛОГИРОВАНИЯ                                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  1. ИСПОЛЬЗУЙТЕ уровни по назначению:                            ║
║     DEBUG   — детали для отладки                                ║
║     INFO    — ключевые события (запуск, запросы)                 ║
║     WARNING — потенциальные проблемы                             ║
║     ERROR   — ошибки, требующие внимания                         ║
║     CRITICAL — критические сбои                                  ║
║                                                                  ║
║  2. СОЗДАВАЙТЕ логгеры через getLogger(__name__)                 ║
║     (не используйте root logger напрямую)                        ║
║                                                                  ║
║  3. НЕ ЛОГИРУЙТЕ sensitive data (пароли, токены)                 ║
║                                                                  ║
║  4. ИСПОЛЬЗУЙТЕ ротацию логов (RotatingFileHandler)              ║
║                                                                  ║
║  5. СТРУКТУРНОЕ логирование (JSON) для production                ║
║                                                                  ║
║  6. ДОБАВЛЯЙТЕ request_id для отслеживания цепочек               ║
║                                                                  ║
║  7. НЕ ИСПОЛЬЗУЙТЕ print() для логов!                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    basic_logging_demo()
    advanced_logging_demo()
    structured_logging_demo()
    decorator_logging_demo()
    print(BEST_PRACTICES)

    print("=" * 60)
    print("✅ УРОК 29 ЗАВЕРШЁН: ЛОГИРОВАНИЕ ОСВОЕНО!")
    print("=" * 60)
