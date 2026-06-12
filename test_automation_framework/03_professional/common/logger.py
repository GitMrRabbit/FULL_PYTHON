"""Модуль логирования для тестового фреймворка.

Поддерживает:
  - Логирование в файл с ротацией
  - Вывод в консоль
  - Структурный JSON-формат (опционально)
  - Разные уровни для файла и консоли
"""

import logging
import logging.handlers
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


class JsonFormatter(logging.Formatter):
    """Форматтер для структурного логирования в JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = str(record.exc_info[1])

        # Дополнительные поля из extra
        extra_fields = {"test_name", "browser", "environment"}
        for field in extra_fields:
            if hasattr(record, field):
                log_entry[field] = getattr(record, field)

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logger(
    name: str = "test_framework",
    log_dir: str = "logs",
    level: int = logging.DEBUG,
    console_level: int = logging.INFO,
    use_json: bool = False,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Создаёт и настраивает логгер.

    Args:
        name: Имя логгера.
        log_dir: Директория для файлов логов.
        level: Уровень для файлового handler.
        console_level: Уровень для консольного handler.
        use_json: Использовать JSON-формат.
        max_bytes: Максимальный размер файла лога.
        backup_count: Количество файлов ротации.

    Returns:
        Настроенный логгер.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Очищаем существующие handlers (на случай повторного вызова)
    logger.handlers.clear()

    # Директория для логов
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Форматтеры
    if use_json:
        file_formatter = JsonFormatter()
        console_formatter = JsonFormatter()
    else:
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] %(name)s:%(funcName)s:%(lineno)d — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_formatter = logging.Formatter(
            "[%(levelname)-8s] %(name)s — %(message)s"
        )

    # Файловый handler с ротацией
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / f"{name}.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Консольный handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Получить логгер (создаёт базовый если ещё нет).

    Args:
        name: Имя логгера (по умолчанию __name__ вызывающего модуля).

    Returns:
        Логгер.
    """
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get("__name__", "unknown")

    logger = logging.getLogger(name)

    # Если логгер не настроен, добавляем базовый handler
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            "[%(levelname)-8s] %(name)s — %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
