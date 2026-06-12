# 🎭 Урок 19: Декораторы

## 📖 Теория

Декоратор — функция, которая принимает другую функцию и расширяет её поведение без изменения кода самой функции.

```python
@my_decorator
def my_function():
    ...
# Эквивалентно: my_function = my_decorator(my_function)
```

---

## 🔹 Замыкания (Closures) — основа декораторов

```python
def make_multiplier(factor):
    def multiplier(x):
        return x * factor    # factor — из замыкания
    return multiplier

double = make_multiplier(2)
double(5)  # 10
```

---

## 🔹 Простой декоратор

```python
import functools

def logger(func):
    @functools.wraps(func)  # Сохраняет __name__, __doc__!
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"  → {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(3, 4)
# Вызов add((3, 4), {})
#   → 7
```

---

## 🔹 Декоратор с аргументами

```python
def repeat(times):              # Фабрика (получает аргумент)
    def decorator(func):        # Декоратор (получает функцию)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # Обёртка
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello(name):
    print(f"Hello, {name}!")
# Трёхуровневая вложенность: фабрика → декоратор → обёртка
```

---

## 🔹 Класс как декоратор

```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hello, {name}"
```

---

## 🔹 Цепочки декораторов

```python
@bold        # Применяется ВТОРЫМ: bold(italic_result)
@italic      # Применяется ПЕРВЫМ: italic(func_result)
def text():
    return "Hello"

# Эквивалентно: bold(italic(text))
# Результат: <b><i>Hello</i></b>
```

---

## 🔹 Популярные применения

| Декоратор | Назначение |
|-----------|-----------|
| `@timer` | Замер времени выполнения |
| `@retry` | Повтор при ошибке |
| `@cache` / `@lru_cache` | Мемоизация (кеширование) |
| `@log` | Логирование вызовов |
| `@validate_types` | Проверка типов аргументов |
| `@deprecated` | Предупреждение об устаревании |
| `@authenticated` | Проверка аутентификации |
| `@staticmethod` / `@classmethod` | Встроенные! |

---

## ⚠️ `@functools.wraps` — не забывайте!

```python
# ❌ Без @wraps
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func(): """Docstring"""
print(my_func.__name__)  # "wrapper" — не "my_func"!
print(my_func.__doc__)   # None!

# ✅ С @wraps
def good_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 🧪 Упражнения

1. Напишите декоратор `@timeout(seconds)`, ограничивающий время выполнения функции
2. Реализуйте декоратор `@singleton` для класса (только один экземпляр)
3. Создайте декоратор `@log_to_file(filename)`, записывающий логи в файл
4. Напишите декоратор `@rate_limit(calls_per_second)` для ограничения частоты вызовов
