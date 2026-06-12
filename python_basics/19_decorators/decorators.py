"""
Урок 19: Декораторы
====================

Темы:
  - Замыкания (closures)
  - Простые декораторы функций
  - Декораторы с аргументами
  - @functools.wraps — сохранение метаданных
  - Классы как декораторы (__call__)
  - Цепочки декораторов (stacking)
  - Практические примеры: @timer, @retry, @cache, @log
"""

import time
import functools
from typing import Any, Callable


# =============================================================================
# 1. ЗАМЫКАНИЯ (CLOSURES) — ОСНОВА ДЕКОРАТОРОВ
# =============================================================================

def make_multiplier(factor: int):
    """
    Замыкание: внутренняя функция "запоминает" factor из внешней области.
    """
    def multiplier(x: int) -> int:
        return x * factor  # factor — из замыкания
    return multiplier


def make_counter(start: int = 0):
    """Замыкание с изменяемым состоянием."""
    count = start

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def closures_demo():
    """Демонстрация замыканий."""
    print("=" * 60)
    print("1. ЗАМЫКАНИЯ (CLOSURES)")
    print("=" * 60)

    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")

    c1 = make_counter()
    c2 = make_counter(10)
    print(f"c1(): {c1()}, {c1()}, {c1()}")  # 1, 2, 3
    print(f"c2(): {c2()}, {c2()}")          # 11, 12


# =============================================================================
# 2. ПРОСТЫЕ ДЕКОРАТОРЫ
# =============================================================================

def uppercase_decorator(func: Callable) -> Callable:
    """
    Декоратор: принимает функцию, возвращает новую функцию-обёртку.

    Это ТО ЖЕ САМОЕ, что и:
        @uppercase_decorator
        def greet(name): ...
    """
    @functools.wraps(func)  # Сохраняет __name__, __doc__, __module__ и т.д.
    def wrapper(*args, **kwargs) -> Any:
        result = func(*args, **kwargs)
        if isinstance(result, str):
            return result.upper()
        return result
    return wrapper


def log_calls(func: Callable) -> Callable:
    """Декоратор: логирует каждый вызов функции."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        print(f"[LOG] {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        print(f"[LOG]   → {result!r}")
        return result

    return wrapper


@uppercase_decorator
@log_calls
def greet(name: str) -> str:
    """Приветствие."""
    return f"Hello, {name}!"


def simple_decorators_demo():
    """Демонстрация простых декораторов."""
    print("\n" + "=" * 60)
    print("2. ПРОСТЫЕ ДЕКОРАТОРЫ")
    print("=" * 60)

    result = greet("World")
    print(f"Итог: {result}")
    print(f"greet.__name__ = {greet.__name__}")  # "greet" благодаря @wraps
    print(f"greet.__doc__  = {greet.__doc__}")   # "Приветствие."


# =============================================================================
# 3. ДЕКОРАТОРЫ С АРГУМЕНТАМИ
# =============================================================================

def repeat(times: int):
    """
    Декоратор с аргументом: @repeat(3).
    Фабрика декораторов: внешняя функция получает аргумент,
    средняя — функцию, внутренняя — аргументы функции.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = None
            for i in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def retry(max_attempts: int = 3, delay: float = 0.5, exceptions: tuple = (Exception,)):
    """Декоратор: повторяет функцию при ошибке с задержкой."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if attempt < max_attempts:
                        print(f"[RETRY] Попытка {attempt}/{max_attempts} "
                              f"для {func.__name__}: {e}. Ждём {delay}с...")
                        time.sleep(delay)
            raise last_error  # Все попытки исчерпаны
        return wrapper
    return decorator


@repeat(3)
def say_hello(name: str) -> str:
    """Скажет Hello 3 раза (вызывается 3 раза внутри декоратора)."""
    print(f"  Вызов say_hello({name!r})")
    return f"Hello, {name}!"


@retry(max_attempts=3, delay=0.1)
def unstable_function() -> str:
    """
    Функция, которая падает первые 2 раза, а на 3-й работает.
    (Для демонстрации — использует глобальный счётчик.)
    """
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError(f"Попытка {call_count}: нет соединения")
    return "Успех!"


call_count = 0  # Глобальный счётчик для демонстрации retry


def decorators_with_args_demo():
    """Демонстрация декораторов с аргументами."""
    print("\n" + "=" * 60)
    print("3. ДЕКОРАТОРЫ С АРГУМЕНТАМИ")
    print("=" * 60)

    print("repeat(3):")
    result = say_hello("World")
    print(f"Итог: {result}")

    global call_count
    call_count = 0
    print(f"\nretry(max_attempts=3):")
    try:
        result = unstable_function()
        print(f"Итог: {result}")
    except ConnectionError as e:
        print(f"Не удалось: {e}")


# =============================================================================
# 4. КЛАССЫ КАК ДЕКОРАТОРЫ
# =============================================================================

class CountCalls:
    """Декоратор-класс: считает количество вызовов функции."""

    def __init__(self, func: Callable):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs) -> Any:
        self.count += 1
        print(f"[COUNT] {self.func.__name__} вызвана {self.count} раз(а)")
        return self.func(*args, **kwargs)


class Timer:
    """Декоратор-класс с аргументом: @Timer(prefix='[TIME]')."""

    def __init__(self, prefix: str = "[TIMER]"):
        self.prefix = prefix

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"{self.prefix} {func.__name__}: {elapsed:.6f} сек")
            return result
        return wrapper


@CountCalls
def say_hi(name: str) -> str:
    return f"Hi, {name}!"


@Timer(prefix="⏱")
def slow_calculation(n: int) -> int:
    """Медленное вычисление (для демонстрации Timer)."""
    total = 0
    for i in range(n):
        total += i ** 2
    return total


def class_decorators_demo():
    """Демонстрация классов как декораторов."""
    print("\n" + "=" * 60)
    print("4. КЛАССЫ КАК ДЕКОРАТОРЫ")
    print("=" * 60)

    print(f"say_hi('Alice'): {say_hi('Alice')}")
    print(f"say_hi('Bob'):   {say_hi('Bob')}")
    print(f"Всего вызовов: {say_hi.count}")

    result = slow_calculation(1_000_000)
    print(f"Результат: {result}")


# =============================================================================
# 5. ПРАКТИЧЕСКИЕ ПРИМЕРЫ ДЕКОРАТОРОВ
# =============================================================================

def cache(func: Callable) -> Callable:
    """
    Мемоизация: кеширует результаты вызовов.
    Для простых хешируемых аргументов.
    """
    memo: dict = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in memo:
            memo[args] = func(*args)
        else:
            print(f"  [CACHE HIT] {func.__name__}{args} → {memo[args]}")
        return memo[args]

    # Метод для очистки кеша
    wrapper.cache_clear = lambda: memo.clear()
    wrapper.cache_info = lambda: f"Cache: {len(memo)} entries"

    return wrapper


def validate_types(**type_hints):
    """
    Декоратор для проверки типов аргументов.

    @validate_types(a=int, b=int)
    def add(a, b): ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем имена аргументов
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for name, expected_type in type_hints.items():
                if name in bound.arguments:
                    value = bound.arguments[name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{func.__name__}: параметр '{name}' "
                            f"должен быть {expected_type.__name__}, "
                            f"получен {type(value).__name__} ({value!r})"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


@cache
def fibonacci(n: int) -> int:
    """Рекурсивный Фибоначчи с кешированием."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@validate_types(a=int, b=int)
def safe_add(a, b):
    return a + b


def practical_decorators_demo():
    """Демонстрация практических декораторов."""
    print("\n" + "=" * 60)
    print("5. ПРАКТИЧЕСКИЕ ПРИМЕРЫ")
    print("=" * 60)

    print("Кешированный Фибоначчи:")
    print(f"  fibonacci(10) = {fibonacci(10)}")
    print(f"  fibonacci(10) = {fibonacci(10)}")  # Cache hit
    print(f"  {fibonacci.cache_info()}")

    fibonacci.cache_clear()

    print(f"\nВалидация типов:")
    print(f"  safe_add(3, 4) = {safe_add(3, 4)}")
    try:
        safe_add("3", 4)
    except TypeError as e:
        print(f"  [!] {e}")


# =============================================================================
# 6. ЦЕПОЧКИ ДЕКОРАТОРОВ
# =============================================================================

def bold(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper


def italic(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper


@bold
@italic
def format_text(text: str) -> str:
    """
    Порядок:
      1. @italic: format_text → <i>text</i>
      2. @bold:   <b><i>text</i></b>
    """
    return text


def decorator_stacking_demo():
    """Демонстрация цепочек декораторов."""
    print("\n" + "=" * 60)
    print("6. ЦЕПОЧКИ ДЕКОРАТОРОВ")
    print("=" * 60)

    result = format_text("Hello!")
    print(f"@bold @italic: {result}")
    # Эквивалентно: bold(italic(format_text))("Hello!")


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    closures_demo()
    simple_decorators_demo()
    decorators_with_args_demo()
    class_decorators_demo()
    practical_decorators_demo()
    decorator_stacking_demo()

    print("\n" + "=" * 60)
    print("✅ УРОК 19 ЗАВЕРШЁН: ДЕКОРАТОРЫ ОСВОЕНЫ!")
    print("=" * 60)
