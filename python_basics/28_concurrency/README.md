# ⚡ Урок 28: Асинхронность и параллелизм

## 📖 Три способа конкурентности

| Инструмент | Для чего | GIL? |
|-----------|----------|------|
| `threading` | I/O-bound (сеть, файлы) | Да, но для I/O не мешает |
| `asyncio` | I/O-bound (сеть, БД) | Нет (один поток) |
| `multiprocessing` | CPU-bound (вычисления) | Обходит GIL |

---

## 🔹 threading

```python
import threading

t = threading.Thread(target=io_task, args=("Task",))
t.start()
t.join()  # Ждать завершения
```

---

## 🔹 concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(task, arg) for arg in args]
    results = [f.result() for f in futures]
```

---

## 🔹 asyncio

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)  # Имитация I/O
    return f"Result: {url}"

async def main():
    results = await asyncio.gather(fetch("a"), fetch("b"))

asyncio.run(main())
```

---

## 🔹 Lock (блокировка)

```python
lock = threading.Lock()

with lock:
    counter += 1  # Безопасно!
```

---

## 📊 Когда что использовать

- **threading + futures** — простой I/O (файлы, API)
- **asyncio** — много сетевых соединений (веб-сервер, чат)
- **multiprocessing** — CPU-тяжёлые вычисления

## 🧪 Упражнения

1. Загрузите 10 URL параллельно через ThreadPoolExecutor
2. Реализуйте producer-consumer через asyncio.Queue
3. Посчитайте простые числа через ProcessPoolExecutor
