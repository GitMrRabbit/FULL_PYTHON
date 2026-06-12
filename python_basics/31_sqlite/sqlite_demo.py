"""
Урок 31: SQLite в Python
=========================

Темы:
  - Подключение к БД: sqlite3.connect()
  - Создание таблиц (CREATE TABLE)
  - CRUD: INSERT, SELECT, UPDATE, DELETE
  - Параметризованные запросы (? плейсхолдеры)
  - Транзакции (BEGIN, COMMIT, ROLLBACK)
  - RowFactory (доступ по именам колонок)
  - Связи: JOIN (INNER, LEFT)
  - Миграции схемы
"""

import sqlite3
from pathlib import Path
from typing import Optional


# =============================================================================
# 1. ПОДКЛЮЧЕНИЕ И СОЗДАНИЕ ТАБЛИЦ
# =============================================================================

def create_database(db_path: str = ":memory:") -> sqlite3.Connection:
    """
    Создаёт подключение и таблицы.
    :memory: — БД в оперативной памяти (для тестов).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Доступ к колонкам по имени!
    conn.execute("PRAGMA foreign_keys = ON")  # Включаем внешние ключи

    cursor = conn.cursor()

    # Создание таблиц
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'todo',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        -- Индексы для часто запрашиваемых полей
        CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
    """)

    conn.commit()
    return conn


def basic_demo():
    """Демонстрация базовых операций."""
    print("=" * 60)
    print("1. БАЗОВЫЕ ОПЕРАЦИИ")
    print("=" * 60)

    conn = create_database()

    # --- INSERT (параметризованный запрос) ---
    # НИКОГДА не используйте f-строки для SQL! Только ? плейсхолдеры!
    conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Анна", "anna@example.com")
    )
    conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Борис", "boris@example.com")
    )

    # INSERT с RETURNING (SQLite 3.35+)
    cursor = conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?) RETURNING id",
        ("Вера", "vera@example.com")
    )
    new_id = cursor.fetchone()["id"]
    print(f"Добавлен пользователь с id={new_id}")

    # INSERT многих записей
    users_data = [
        ("Глеб", "gleb@example.com"),
        ("Диана", "diana@example.com"),
    ]
    conn.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        users_data
    )
    print(f"Добавлено пользователей: {len(users_data)}")

    # --- SELECT ---
    print("\nВсе пользователи:")
    for row in conn.execute("SELECT id, name, email FROM users ORDER BY id"):
        print(f"  #{row['id']}: {row['name']} <{row['email']}>")

    # SELECT с условием
    cursor = conn.execute(
        "SELECT * FROM users WHERE name LIKE ?",
        ("%ан%",)  # Имена содержащие "ан"
    )
    print(f"\nПользователи с 'ан' в имени:")
    for row in cursor:
        print(f"  {row['name']}")

    # --- UPDATE ---
    conn.execute(
        "UPDATE users SET name = ? WHERE id = ?",
        ("Анна Смирнова", 1)
    )
    print(f"\nОбновлён пользователь #1")

    # --- DELETE ---
    conn.execute("DELETE FROM users WHERE id = ?", (5,))
    print(f"Удалён пользователь #5")

    conn.close()


# =============================================================================
# 2. ТРАНЗАКЦИИ
# =============================================================================

def transactions_demo():
    """Демонстрация транзакций."""
    print("\n" + "=" * 60)
    print("2. ТРАНЗАКЦИИ")
    print("=" * 60)

    conn = create_database()

    # Успешная транзакция
    try:
        conn.execute("BEGIN")
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                     ("Транзакция", "tx@example.com"))
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                     ("Успех", "success@example.com"))
        conn.execute("COMMIT")
        print("[OK] Транзакция закоммичена")
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"[!] Откат: {e}")

    # Транзакция с ошибкой
    try:
        conn.execute("BEGIN")
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                     ("Ошибка", "error@example.com"))
        # Дубликат email → UNIQUE constraint violation
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                     ("Дубль", "error@example.com"))
        conn.execute("COMMIT")
    except sqlite3.IntegrityError as e:
        conn.execute("ROLLBACK")
        print(f"[!] Откат из-за: {e}")

    # Проверяем — запись "Ошибка" не добавлена (откат)
    count = conn.execute("SELECT COUNT(*) as cnt FROM users WHERE name = 'Ошибка'").fetchone()
    print(f"Записей 'Ошибка' в БД: {count['cnt']} (должно быть 0)")

    conn.close()


# =============================================================================
# 3. JOIN И СВЯЗИ
# =============================================================================

def joins_demo():
    """Демонстрация JOIN."""
    print("\n" + "=" * 60)
    print("3. JOIN")
    print("=" * 60)

    conn = create_database()

    # Добавляем данные
    conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Анна", "anna@example.com"))
    conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Борис", "boris@example.com"))

    user1_id = conn.execute("SELECT id FROM users WHERE name = 'Анна'").fetchone()["id"]
    user2_id = conn.execute("SELECT id FROM users WHERE name = 'Борис'").fetchone()["id"]

    conn.executemany(
        "INSERT INTO tasks (user_id, title, status) VALUES (?, ?, ?)",
        [
            (user1_id, "Написать отчёт", "done"),
            (user1_id, "Проверить тесты", "in_progress"),
            (user2_id, "Обновить документацию", "todo"),
        ]
    )

    # INNER JOIN — только связанные записи
    print("INNER JOIN (задачи с пользователями):")
    for row in conn.execute("""
        SELECT u.name, t.title, t.status
        FROM users u
        INNER JOIN tasks t ON u.id = t.user_id
        ORDER BY u.name, t.title
    """):
        print(f"  {row['name']:10s} | {row['title']:25s} | {row['status']}")

    # LEFT JOIN — все пользователи, даже без задач
    print("\nLEFT JOIN (все пользователи):")
    for row in conn.execute("""
        SELECT u.name, COUNT(t.id) as task_count
        FROM users u
        LEFT JOIN tasks t ON u.id = t.user_id
        GROUP BY u.id
        ORDER BY task_count DESC
    """):
        print(f"  {row['name']:10s}: {row['task_count']} задач(и)")

    conn.close()


# =============================================================================
# 4. РЕПОЗИТОРИЙ (ПРАКТИЧЕСКИЙ ПРИМЕР)
# =============================================================================

class UserRepository:
    """Репозиторий для работы с пользователями через SQLite."""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER CHECK (age >= 0 AND age <= 150)
            )
        """)
        self.conn.commit()

    def create(self, name: str, email: str, age: int) -> dict:
        cursor = self.conn.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (name, email, age)
        )
        self.conn.commit()
        return {"id": cursor.lastrowid, "name": name, "email": email, "age": age}

    def get_by_id(self, user_id: int) -> dict | None:
        row = self.conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_all(self, limit: int = 100) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM users ORDER BY id LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def update(self, user_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values()) + [user_id]
        self.conn.execute(f"UPDATE users SET {sets} WHERE id = ?", values)
        self.conn.commit()
        return True

    def delete(self, user_id: int) -> bool:
        cursor = self.conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) as cnt FROM users").fetchone()["cnt"]

    def close(self):
        self.conn.close()


def repository_demo():
    """Демонстрация репозитория."""
    print("\n" + "=" * 60)
    print("4. РЕПОЗИТОРИЙ")
    print("=" * 60)

    repo = UserRepository()

    repo.create("Анна", "anna@example.com", 28)
    repo.create("Борис", "boris@example.com", 35)
    repo.create("Вера", "vera@example.com", 22)

    print(f"Всего пользователей: {repo.count()}")
    print("Все пользователи:")
    for user in repo.get_all():
        print(f"  #{user['id']}: {user['name']} ({user['age']} лет)")

    user = repo.get_by_id(1)
    print(f"\nПользователь #1: {user['name']}")

    repo.update(1, name="Анна Смирнова", age=29)
    user = repo.get_by_id(1)
    print(f"После обновления: {user['name']} ({user['age']} лет)")

    repo.delete(3)
    print(f"После удаления: {repo.count()} пользователей")

    repo.close()


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    basic_demo()
    transactions_demo()
    joins_demo()
    repository_demo()

    print("\n" + "=" * 60)
    print("✅ УРОК 31 ЗАВЕРШЁН: SQLITE ОСВОЕНА!")
    print("=" * 60)
