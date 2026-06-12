"""
Урок 32: PostgreSQL в Python
=============================

Темы:
  - Установка и подключение (psycopg2 / psycopg3)
  - Connection string (DSN)
  - Параметризованные запросы (%s плейсхолдеры)
  - Connection Pooling (psycopg2.pool)
  - Транзакции и уровни изоляции
  - JSONB, массивы — специфика PostgreSQL
  - Миграции (Alembic — обзор)
  - Отличия от SQLite

⚠️ Требуется установленный PostgreSQL и библиотека psycopg2:
    pip install psycopg2-binary
"""

# =============================================================================
# ВАЖНО: Этот код НЕ запустится без PostgreSQL!
# Раскомментируйте и адаптируйте под ваше окружение.
# =============================================================================

POSTGRESQL_SETUP = """
╔══════════════════════════════════════════════════════════════════╗
║  УСТАНОВКА POSTGRESQL                                            ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  # Windows: скачать с https://www.postgresql.org/download/      ║
║  # Linux:   sudo apt install postgresql                         ║
║  # Mac:     brew install postgresql                             ║
║  # Docker:  docker run -d --name pg -e POSTGRES_PASSWORD=pass   ║
║  #           -p 5432:5432 postgres:16                            ║
║                                                                  ║
║  # Установка драйвера                                            ║
║  pip install psycopg2-binary                                     ║
║                                                                  ║
║  # Создание БД (в psql или pgAdmin)                             ║
║  CREATE DATABASE mydb;                                           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

# =============================================================================
# 1. ПОДКЛЮЧЕНИЕ
# =============================================================================

def connection_example():
    """
    Пример подключения к PostgreSQL.

    DSN (Data Source Name) — строка подключения.
    """
    # Пример кода (НЕ запустится без PostgreSQL!)
    example_code = '''
import psycopg2
from psycopg2 import pool

# Простое подключение
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydb",
    user="postgres",
    password="your_password"
)

# Или через DSN-строку
conn = psycopg2.connect(
    "host=localhost port=5432 dbname=mydb user=postgres password=your_password"
)

# Connection Pool (пул соединений) — для production!
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host="localhost",
    port=5432,
    database="mydb",
    user="postgres",
    password="your_password"
)

# Взять соединение из пула
conn = connection_pool.getconn()
# ... работа с БД ...
# Вернуть соединение в пул
connection_pool.putconn(conn)
'''
    print("=" * 60)
    print("1. ПОДКЛЮЧЕНИЕ К POSTGRESQL")
    print("=" * 60)
    print(example_code)


# =============================================================================
# 2. CRUD ОПЕРАЦИИ
# =============================================================================

def crud_example():
    """
    Примеры CRUD с PostgreSQL.
    Плейсхолдер %s (вместо ? в SQLite).
    """
    example_code = '''
# --- Создание таблиц ---
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
        attributes JSONB DEFAULT '{}',
        tags TEXT[] DEFAULT '{}',
        created_at TIMESTAMP DEFAULT NOW()
    );
""")
conn.commit()

# --- INSERT ---
cursor.execute(
    "INSERT INTO products (name, price, attributes, tags) VALUES (%s, %s, %s, %s) RETURNING id",
    ("Ноутбук", 50000.00, '{"brand": "Dell", "cpu": "i7"}', ["электроника", "компьютеры"])
)
new_id = cursor.fetchone()[0]
print(f"Добавлен продукт #{new_id}")

# INSERT многих записей
products_data = [
    ("Мышь", 2000.00, '{"wireless": true}', ["периферия"]),
    ("Клавиатура", 3500.00, '{"mechanical": true}', ["периферия"]),
]
cursor.executemany(
    "INSERT INTO products (name, price, attributes, tags) VALUES (%s, %s, %s, %s)",
    products_data
)

# --- SELECT ---
cursor.execute("SELECT id, name, price, tags FROM products ORDER BY price DESC")
for row in cursor.fetchall():
    print(f"  #{row[0]}: {row[1]} — {row[2]} ₽ {row[3]}")

# --- SELECT с JSONB ---
cursor.execute("""
    SELECT name, attributes->>'brand' as brand
    FROM products
    WHERE attributes @> '{"wireless": true}'
""")

# --- UPDATE ---
cursor.execute(
    "UPDATE products SET price = %s WHERE id = %s",
    (45000.00, 1)
)

# --- DELETE ---
cursor.execute("DELETE FROM products WHERE id = %s", (3,))

conn.commit()
cursor.close()
'''
    print("\n" + "=" * 60)
    print("2. CRUD ОПЕРАЦИИ")
    print("=" * 60)
    print(example_code)


# =============================================================================
# 3. ТРАНЗАКЦИИ
# =============================================================================

def transactions_example():
    """Примеры транзакций в PostgreSQL."""
    example_code = '''
# Автоматическая транзакция (autocommit=False по умолчанию)
conn.autocommit = False

try:
    cursor.execute("INSERT INTO users (name) VALUES (%s)", ("Alice",))
    cursor.execute("INSERT INTO users (name) VALUES (%s)", ("Bob",))
    conn.commit()  # Подтверждаем
except Exception as e:
    conn.rollback()  # Откатываем
    print(f"Ошибка: {e}")

# Уровни изоляции
from psycopg2.extensions import (
    ISOLATION_LEVEL_READ_COMMITTED,   # По умолчанию
    ISOLATION_LEVEL_REPEATABLE_READ,
    ISOLATION_LEVEL_SERIALIZABLE,
)
conn.set_isolation_level(ISOLATION_LEVEL_SERIALIZABLE)

# Контекстный менеджер
with conn:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO logs (message) VALUES (%s)", ("Запись",))
# Автоматический commit при выходе из with!
'''
    print("\n" + "=" * 60)
    print("3. ТРАНЗАКЦИИ")
    print("=" * 60)
    print(example_code)


# =============================================================================
# 4. ОСОБЕННОСТИ POSTGRESQL
# =============================================================================

def postgresql_features():
    """Уникальные фичи PostgreSQL."""
    features = """
╔══════════════════════════════════════════════════════════════════╗
║  POSTGRESQL УНИКАЛЬНЫЕ ФИЧИ (vs SQLite)                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  JSONB — бинарный JSON с индексацией и запросами:                ║
║    CREATE INDEX idx_attrs ON products USING GIN (attributes);    ║
║    SELECT * FROM products WHERE attributes @> '{"brand":"Dell"}';║
║                                                                  ║
║  ARRAY — массивы как тип колонки:                                ║
║    tags TEXT[] DEFAULT '{}'                                      ║
║    SELECT * FROM products WHERE 'electronics' = ANY(tags);        ║
║                                                                  ║
║  FULL-TEXT SEARCH (полнотекстовый поиск):                        ║
║    CREATE INDEX idx_fts ON products USING GIN(                   ║
║      to_tsvector('russian', name || ' ' || description)          ║
║    );                                                            ║
║    SELECT * FROM products                                        ║
║    WHERE to_tsvector('russian', name) @@ to_tsquery('ноутбук');  ║
║                                                                  ║
║  WINDOW FUNCTIONS:                                               ║
║    SELECT name, price,                                           ║
║           RANK() OVER (ORDER BY price DESC) as rank              ║
║    FROM products;                                                ║
║                                                                  ║
║  CTE (WITH ...):                                                 ║
║    WITH expensive AS (                                           ║
║      SELECT * FROM products WHERE price > 10000                  ║
║    )                                                             ║
║    SELECT name FROM expensive WHERE tags @> ARRAY['electronics'];║
║                                                                  ║
║  UPSERT (INSERT ... ON CONFLICT):                                ║
║    INSERT INTO users (email, name) VALUES ('a@mail.com', 'A')    ║
║    ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print("\n" + "=" * 60)
    print("4. ОСОБЕННОСТИ POSTGRESQL")
    print("=" * 60)
    print(features)


# =============================================================================
# 5. МИГРАЦИИ (ALEMBIC)
# =============================================================================

def migrations_info():
    """Информация о миграциях."""
    info = """
╔══════════════════════════════════════════════════════════════════╗
║  МИГРАЦИИ СХЕМЫ БД (Alembic)                                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Установка: pip install alembic                                  ║
║                                                                  ║
║  # Инициализация                                                 ║
║  alembic init alembic                                            ║
║                                                                  ║
║  # Создание миграции                                             ║
║  alembic revision --autogenerate -m "add users table"            ║
║                                                                  ║
║  # Применение миграций                                           ║
║  alembic upgrade head                                            ║
║                                                                  ║
║  # Откат                                                         ║
║  alembic downgrade -1                                            ║
║                                                                  ║
║  Структура миграции:                                             ║
║  def upgrade():                                                  ║
║      op.create_table('users', ...)                               ║
║                                                                  ║
║  def downgrade():                                                ║
║      op.drop_table('users')                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print("\n" + "=" * 60)
    print("5. МИГРАЦИИ (ALEMBIC)")
    print("=" * 60)
    print(info)


# =============================================================================
# 6. СРАВНЕНИЕ SQLITE vs POSTGRESQL
# =============================================================================

COMPARISON = """
╔═══════════════════╦═════════════════════╦═════════════════════════════╗
║ Характеристика    ║ SQLite              ║ PostgreSQL                  ║
╠═══════════════════╬═════════════════════╬═════════════════════════════╣
║ Тип               ║ Встраиваемая (файл) ║ Клиент-серверная            ║
║ Установка         ║ Не нужна             ║ Требуется                   ║
║ Конкурентность    ║ Ограниченная         ║ Высокая (MVCC)              ║
║ Типы данных       ║ 5 типов              ║ 40+ (JSONB, ARRAY, UUID)   ║
║ Размер БД         ║ До 281 ТБ            ║ Не ограничен               ║
║ Пользователи/Роли ║ Нет                  ║ Полноценная система прав   ║
║ Репликация        ║ Нет                  ║ Master-Slave, Streaming    ║
║ Полнотекст. поиск ║ Ограничен (FTS5)     ║ Полноценный                ║
║ Для чего          ║ Прототипы, mobile,   ║ Production, Web,            ║
║                   ║ маленькие проекты    ║ высокая нагрузка           ║
║ Плейсхолдер       ║ ?                    ║ %s                         ║
║ Автоинкремент     ║ INTEGER PK           ║ SERIAL / IDENTITY          ║
╚═══════════════════╩═════════════════════╩═════════════════════════════╝
"""


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    print(POSTGRESQL_SETUP)
    connection_example()
    crud_example()
    transactions_example()
    postgresql_features()
    migrations_info()
    print(COMPARISON)

    print("=" * 60)
    print("✅ УРОК 32 ЗАВЕРШЁН: POSTGRESQL ОСВОЕН!")
    print("=" * 60)
    print()
    print("🎉 ПОЗДРАВЛЯЮ! ВЫ ОСВОИЛИ ВСЕ 32 УРОКА PYTHON!")
