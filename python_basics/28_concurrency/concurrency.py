"""
Урок 28: Асинхронность и параллелизм в Python
==============================================

Темы:
  - threading — потоки (I/O-bound задачи)
  - multiprocessing — процессы (CPU-bound задачи)
  - asyncio — асинхронное программирование (async/await)
  - concurrent.futures — высокоуровневый API
  - Гонки данных, блокировки (Lock, Semaphore)
  - Выбор правильного инструмента
"""

import time
import threading
import multiprocessing
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable


# =============================================================================
# 1. THREADING — ПОТОКИ
# =============================================================================

def io_task(name: str, delay: float) -> str:
    """Имитация I/O-операции (сеть, файлы, БД)."""
    print(f"  [{name}] Начало (поток {threading.current_thread().name})")
    time.sleep(delay)
    print(f"  [{name}] Конец")
    return f"Результат {name}"


def threading_demo():
    """Демонстрация потоков (GIL ограничивает CPU, но не I/O)."""
    print("=" * 60)
    print("1. THREADING — ПОТОКИ")
    print("=" * 60)

    start = time.perf_counter()

    # Создание потоков
    threads = [
        threading.Thread(target=io_task, args=(f"Task-{i}", 0.5))
        for i in range(5)
    ]

    # Запуск
    for t in threads:
        t.start()

    # Ожидание завершения
    for t in threads:
        t.join()

    elapsed = time.perf_counter() - start
    print(f"Всего: {elapsed:.2f} сек (при последовательном было бы ~2.5 сек)")

    # Демон (daemon) поток — убивается при завершении главного
    daemon = threading.Thread(target=lambda: time.sleep(10), daemon=True)
    daemon.start()


# =============================================================================
# 2. CONCURRENT.FUTURES — ПУЛЫ ПОТОКОВ/ПРОЦЕССОВ
# =============================================================================

def cpu_task(n: int) -> int:
    """CPU-bound задача: вычисление простых чисел."""
    count = 0
    for i in range(2, n + 1):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


def concurrent_futures_demo():
    """Демонстрация ThreadPoolExecutor и ProcessPoolExecutor."""
    print("\n" + "=" * 60)
    print("2. CONCURRENT.FUTURES")
    print("=" * 60)

    # ThreadPoolExecutor — для I/O-bound
    print("ThreadPoolExecutor (I/O):")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(io_task, f"IO-{i}", 0.3) for i in range(5)]
        results = [f.result() for f in futures]
    print(f"  Результаты: {results}")
    print(f"  Время: {time.perf_counter() - start:.2f} сек")

    # ProcessPoolExecutor — для CPU-bound
    print("\nProcessPoolExecutor (CPU):")
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_task, 50000) for _ in range(4)]
        results = [f.result() for f in futures]
    print(f"  Количество простых чисел (до 50000): {results}")
    print(f"  Время: {time.perf_counter() - start:.2f} сек")

    # map — удобный способ
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(lambda x: x ** 2, range(5)))
    print(f"\nexecutor.map: {results}")


# =============================================================================
# 3. ASYNCIO — АСИНХРОННОСТЬ
# =============================================================================

async def async_task(name: str, delay: float) -> str:
    """Асинхронная задача."""
    print(f"  [{name}] Начало")
    await asyncio.sleep(delay)  # Не блокирует event loop!
    print(f"  [{name}] Конец")
    return f"Результат {name}"


async def async_main():
    """Главная асинхронная функция."""
    # Последовательный запуск
    r1 = await async_task("Seq-1", 0.3)
    print(f"  {r1}")

    # Параллельный запуск (asyncio.gather)
    print("\n  Параллельно:")
    results = await asyncio.gather(
        async_task("Par-1", 0.3),
        async_task("Par-2", 0.3),
        async_task("Par-3", 0.3),
    )
    print(f"  Все результаты: {results}")

    # asyncio.create_task — создать задачу и не ждать сразу
    task1 = asyncio.create_task(async_task("Task-1", 0.5))
    task2 = asyncio.create_task(async_task("Task-2", 0.3))
    print("  Задачи созданы, делаем что-то ещё...")
    r1, r2 = await task1, await task2
    print(f"  {r1}, {r2}")


async def async_producer_consumer():
    """Паттерн producer-consumer через asyncio.Queue."""
    queue = asyncio.Queue(maxsize=5)

    async def producer():
        for i in range(5):
            await asyncio.sleep(0.2)
            await queue.put(f"item-{i}")
            print(f"  [Producer] положил item-{i}")

    async def consumer():
        while True:
            item = await queue.get()
            print(f"  [Consumer] обработал {item}")
            queue.task_done()
            if item == "item-4":
                break

    await asyncio.gather(producer(), consumer())


def asyncio_demo():
    """Демонстрация asyncio."""
    print("\n" + "=" * 60)
    print("3. ASYNCIO (async/await)")
    print("=" * 60)

    start = time.perf_counter()
    asyncio.run(async_main())
    print(f"Время async_main: {time.perf_counter() - start:.2f} сек")

    print("\nProducer-Consumer:")
    asyncio.run(async_producer_consumer())


# =============================================================================
# 4. БЛОКИРОВКИ (LOCK)
# =============================================================================

counter = 0
counter_lock = threading.Lock()


def increment_without_lock():
    global counter
    for _ in range(100_000):
        counter += 1


def increment_with_lock():
    global counter
    for _ in range(100_000):
        with counter_lock:  # Безопасно!
            counter += 1


def lock_demo():
    """Демонстрация гонки данных и блокировки."""
    print("\n" + "=" * 60)
    print("4. БЛОКИРОВКИ (Lock)")
    print("=" * 60)

    global counter

    # БЕЗ блокировки — гонка данных (результат непредсказуем!)
    counter = 0
    t1 = threading.Thread(target=increment_without_lock)
    t2 = threading.Thread(target=increment_without_lock)
    t1.start(); t2.start(); t1.join(); t2.join()
    print(f"Без Lock: counter = {counter} (ожидали 200000)")

    # С блокировкой — корректно
    counter = 0
    t1 = threading.Thread(target=increment_with_lock)
    t2 = threading.Thread(target=increment_with_lock)
    t1.start(); t2.start(); t1.join(); t2.join()
    print(f"С Lock:   counter = {counter}")


# =============================================================================
# 5. ВЫБОР ИНСТРУМЕНТА
# =============================================================================

DECISION_MATRIX = """
╔══════════════════════════════════════════════════════════════════╗
║  ЧТО ИСПОЛЬЗОВАТЬ?                                               ║
╠═════════════╦══════════════╦═════════════════════════════════════╣
║ Тип задачи  ║ Инструмент   ║ Причина                            ║
╠═════════════╬══════════════╬═════════════════════════════════════╣
║ I/O-bound   ║ threading    ║ GIL не мешает I/O операциям        ║
║ I/O-bound   ║ asyncio      ║ Ещё эффективнее (один поток)       ║
║ CPU-bound   ║ multiproc.   ║ Обходит GIL — настоящий паралл.   ║
║ Простой API ║ concurrent.   ║ futures — удобная абстракция      ║
╚═════════════╩══════════════╩═════════════════════════════════════╝
"""


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    threading_demo()
    concurrent_futures_demo()
    asyncio_demo()
    lock_demo()

    print("\n" + DECISION_MATRIX)

    print("=" * 60)
    print("✅ УРОК 28 ЗАВЕРШЁН: CONCURRENCY ОСВОЕНА!")
    print("=" * 60)
