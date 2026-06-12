"""
Ответы к упражнениям уроков 20-32
===================================

Генераторы, comprehensions, даты, JSON, regex, БД и др.
Сначала решите САМИ, потом сверяйтесь!
"""

# =============================================================================
# Урок 20: Генераторы
# =============================================================================

# Генератор простых чисел (бесконечный)
def primes():
    """Бесконечный генератор простых чисел."""
    yield 2
    n = 3
    while True:
        is_prime = True
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                is_prime = False
                break
        if is_prime:
            yield n
        n += 2


# Батчирование
def batch(iterable, n: int):
    """Разбивает итератор на батчи размером n."""
    current = []
    for item in iterable:
        current.append(item)
        if len(current) == n:
            yield current
            current = []
    if current:
        yield current


# =============================================================================
# Урок 21: Comprehensions
# =============================================================================

# Простые числа до 100 через comprehension
def primes_up_to_100():
    return [n for n in range(2, 101)
            if all(n % d != 0 for d in range(2, int(n ** 0.5) + 1))]


# Словарь {слово: длина}
def words_length(text: str) -> dict[str, int]:
    return {word: len(word) for word in text.split()}


# Множество гласных
def vowels_in_text(text: str) -> set[str]:
    return {ch.lower() for ch in text if ch.lower() in "aeiouаеёиоуыэюя"}


# Транспонирование матрицы через comprehension
def transpose_comprehension(matrix: list[list]) -> list[list]:
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


# =============================================================================
# Урок 22: Даты и время
# =============================================================================

from datetime import date, timedelta, datetime

def days_to_new_year() -> int:
    today = date.today()
    new_year = date(today.year + 1, 1, 1)
    return (new_year - today).days


def age_in_days(birth_date: date) -> int:
    return (date.today() - birth_date).days


def fridays_13th(year: int) -> list[date]:
    result = []
    for month in range(1, 13):
        d = date(year, month, 13)
        if d.weekday() == 4:  # 0=Пн → 4=Пт
            result.append(d)
    return result


# =============================================================================
# Урок 23: JSON/CSV
# =============================================================================

import json
import csv
from pathlib import Path

def json_to_csv(json_path: str, csv_path: str) -> None:
    with open(json_path, "r", encoding="utf-8") as fj, \
         open(csv_path, "w", newline="", encoding="utf-8") as fc:
        data = json.load(fj)
        if not data:
            return
        writer = csv.DictWriter(fc, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    with open(csv_path, "r", encoding="utf-8") as fc, \
         open(json_path, "w", encoding="utf-8") as fj:
        reader = csv.DictReader(fc)
        data = list(reader)
        json.dump(data, fj, ensure_ascii=False, indent=2)


# =============================================================================
# Урок 24: Regex
# =============================================================================

import re

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_phone_ru(phone: str) -> bool:
    pattern = r"^\+7\s*\(?\d{3}\)?\s*\d{3}[- ]?\d{2}[- ]?\d{2}$"
    return bool(re.match(pattern, phone))


def is_valid_url(url: str) -> bool:
    pattern = (
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?(?:/?|[/?]\S+)$"
    )
    return bool(re.match(pattern, url, re.IGNORECASE))


def extract_dates(text: str) -> list[str]:
    pattern = r"\b\d{2}\.\d{2}\.\d{4}\b"
    return re.findall(pattern, text)


def strip_html_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


# =============================================================================
# Урок 28: Concurrency
# =============================================================================

import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests  # pip install requests

def download_url(url: str) -> tuple[str, int]:
    response = requests.get(url, timeout=10)
    return url, response.status_code


def download_urls_parallel(urls: list[str]) -> list[tuple[str, int]]:
    with ThreadPoolExecutor(max_workers=5) as executor:
        return list(executor.map(download_url, urls))


async def producer(queue: asyncio.Queue):
    for i in range(5):
        await asyncio.sleep(0.5)
        await queue.put(f"item-{i}")
        print(f"  Произведено: item-{i}")


async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        print(f"  Обработано: {item}")
        queue.task_done()
        if item == "item-4":
            break


# =============================================================================
# Урок 29: Logging
# =============================================================================

import logging
import functools
import time as _time

def setup_file_logger(log_dir: str = "logs") -> logging.Logger:
    path = Path(log_dir)
    path.mkdir(exist_ok=True)

    logger = logging.getLogger("my_app")
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(
        path / "app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))
    logger.addHandler(handler)
    return logger


def log_execution(logger: logging.Logger | None = None):
    if logger is None:
        logger = logging.getLogger(__name__)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = _time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed = _time.perf_counter() - start
                logger.debug(f"{func.__name__} → {result!r} ({elapsed:.4f}с)")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} ОШИБКА: {e}")
                raise
        return wrapper
    return decorator


# =============================================================================
# Урок 31: SQLite
# =============================================================================

import sqlite3

def setup_library_db(db_path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            year INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        );
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            borrower TEXT NOT NULL,
            loan_date TEXT DEFAULT (date('now')),
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
    """)
    conn.commit()
    return conn


def get_books_with_authors(conn: sqlite3.Connection) -> list:
    return conn.execute("""
        SELECT b.title, a.name as author, b.year
        FROM books b
        INNER JOIN authors a ON b.author_id = a.id
        ORDER BY b.title
    """).fetchall()


# =============================================================================
# Урок 32: PostgreSQL
# =============================================================================

# Схема (запустите в psql или через Python с psycopg2)
POSTGRES_SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_products_metadata ON products USING GIN (metadata);
CREATE INDEX IF NOT EXISTS idx_products_tags ON products USING GIN (tags);
"""


# =============================================================================
# САМОПРОВЕРКА
# =============================================================================

if __name__ == "__main__":
    print("Проверка ответов к урокам 20-32:\n")

    # Урок 20
    p = primes()
    assert [next(p) for _ in range(5)] == [2, 3, 5, 7, 11]
    assert list(batch([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    print("✓ Урок 20 (Генераторы)")

    # Урок 21
    assert len(primes_up_to_100()) == 25
    assert words_length("hello world") == {"hello": 5, "world": 5}
    assert "a" in vowels_in_text("Hello World")
    print("✓ Урок 21 (Comprehensions)")

    # Урок 22
    assert days_to_new_year() > 0
    print("✓ Урок 22 (Даты)")

    # Урок 24
    assert is_valid_email("alice@example.com") == True
    assert is_valid_email("bad-email") == False
    assert is_valid_phone_ru("+7 (999) 123-45-67") == True
    assert extract_dates("15.06.2024 и 01.01.2025") == ["15.06.2024", "01.01.2025"]
    assert strip_html_tags("<b>Hello</b>") == "Hello"
    print("✓ Урок 24 (Regex)")

    print("\n✅ Все проверки пройдены!")
