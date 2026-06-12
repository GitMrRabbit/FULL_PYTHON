# 🗄️ Урок 31: SQLite в Python

## 📖 Основы

```python
import sqlite3

conn = sqlite3.connect("database.db")     # Файл
conn = sqlite3.connect(":memory:")        # В памяти
conn.row_factory = sqlite3.Row            # Доступ по имени колонки
```

---

## 🔹 CRUD

```python
# INSERT (ВСЕГДА параметризованный!)
conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Анна", "a@mail.com"))

# SELECT
for row in conn.execute("SELECT * FROM users WHERE age > ?", (18,)):
    print(row["name"], row["email"])

# UPDATE
conn.execute("UPDATE users SET name = ? WHERE id = ?", ("Новое имя", 1))

# DELETE
conn.execute("DELETE FROM users WHERE id = ?", (5,))

conn.commit()  # Не забывайте!
```

---

## 🔹 Транзакции

```python
try:
    conn.execute("BEGIN")
    conn.execute("INSERT ...")
    conn.execute("INSERT ...")
    conn.execute("COMMIT")
except:
    conn.execute("ROLLBACK")
```

---

## 🔹 JOIN

```sql
SELECT u.name, t.title
FROM users u
INNER JOIN tasks t ON u.id = t.user_id

SELECT u.name, COUNT(t.id)
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id
```

---

## ⚠️ SQL-инъекции

```python
# ❌ НИКОГДА!
f"SELECT * FROM users WHERE name = '{user_input}'"

# ✅ ВСЕГДА параметризованные запросы!
conn.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```

## 🧪 Упражнения

1. Создайте БД для библиотеки (книги, авторы, выдачи)
2. Реализуйте репозиторий с методами CRUD
3. Напишите запрос с JOIN для отчёта
