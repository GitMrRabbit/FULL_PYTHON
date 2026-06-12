# 🐘 Урок 32: PostgreSQL в Python

## 📖 Установка

```bash
pip install psycopg2-binary

# Docker (быстрый старт)
docker run -d --name pg -e POSTGRES_PASSWORD=pass -p 5432:5432 postgres:16
```

---

## 🔹 Подключение

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432,
    database="mydb", user="postgres", password="pass"
)
```

### Connection Pool (production)

```python
from psycopg2 import pool

pool = pool.SimpleConnectionPool(1, 10, host="localhost", ...)
conn = pool.getconn()
# ... работа ...
pool.putconn(conn)
```

---

## 🔹 CRUD (плейсхолдер %s)

```python
cur = conn.cursor()

# INSERT
cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
            ("Анна", "anna@mail.com"))
new_id = cur.fetchone()[0]

# SELECT
cur.execute("SELECT * FROM users WHERE age > %s", (18,))
for row in cur.fetchall():
    print(row)

# UPDATE / DELETE
cur.execute("UPDATE users SET name = %s WHERE id = %s", ("Новое", 1))
cur.execute("DELETE FROM users WHERE id = %s", (5,))

conn.commit()
```

---

## 🔹 Особенности PostgreSQL

| Фича | Пример |
|------|--------|
| JSONB | `attributes @> '{"key":"value"}'` |
| ARRAY | `'tag' = ANY(tags)` |
| Full-text search | `to_tsvector(name) @@ to_tsquery('word')` |
| UPSERT | `INSERT ... ON CONFLICT DO UPDATE` |
| Window functions | `RANK() OVER (ORDER BY price)` |

---

## 🔹 SQLite vs PostgreSQL

| | SQLite | PostgreSQL |
|---|--------|-----------|
| Тип | Файл | Сервер |
| Конкурентность | Низкая | Высокая (MVCC) |
| Типы данных | 5 | 40+ |
| Для чего | Прототипы, mobile | Production, Web |

---

## 🧪 Упражнения

1. Установите PostgreSQL через Docker
2. Создайте таблицы с внешними ключами и индексами
3. Используйте JSONB для хранения метаданных
4. Настройте Alembic для миграций
