# ⚠️ Урок 13: Исключения в Python

## 📖 Теория

Исключения — это события, возникающие при ошибках выполнения программы. Python предоставляет механизм `try/except` для их обработки, предотвращая аварийное завершение.

---

## 🔹 Иерархия исключений

```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── TypeError
    ├── ValueError
    ├── FileNotFoundError
    ├── ImportError
    ├── AttributeError
    └── ... (многие другие)
```

---

## 🔹 `try` / `except` / `else` / `finally`

```python
try:
    # Код, который МОЖЕТ вызвать исключение
    result = 10 / 0
except ZeroDivisionError:
    # Обработка конкретного исключения
    print("Деление на ноль!")
except (TypeError, ValueError) as e:
    # Несколько типов в одном except
    print(f"Ошибка типа/значения: {e}")
except Exception as e:
    # Общий перехват (ловим всё)
    print(f"Неизвестная ошибка: {e}")
else:
    # Выполняется, если исключений НЕ было
    print(f"Всё хорошо, результат: {result}")
finally:
    # Выполняется ВСЕГДА (даже при return/break/исключении)
    print("Очистка ресурсов...")
```

---

## 🔹 `raise` — выброс исключений

```python
# Простой выброс
raise ValueError("Некорректное значение")

# Повторный выброс (re-raise)
try:
    1 / 0
except ZeroDivisionError:
    print("Логируем ошибку...")
    raise  # Пробрасываем то же исключение дальше

# Выброс с цепочкой (raise ... from ...)
try:
    data = json.loads(invalid_string)
except json.JSONDecodeError as e:
    raise ValueError("Ошибка парсинга конфигурации") from e
# Выводит оба трейсбека: прямое исключение + исходное
```

---

## 🔹 Создание пользовательских исключений

```python
class MyAppError(Exception):
    """Базовое исключение приложения."""
    pass

class ValidationError(MyAppError):
    """Ошибка валидации данных."""
    def __init__(self, field: str, value, message: str = ""):
        self.field = field
        self.value = value
        super().__init__(f"Поле '{field}' = {value!r}: {message}")

class ConfigError(MyAppError):
    """Ошибка конфигурации."""
    pass

# Использование
def validate_age(age):
    if not isinstance(age, int):
        raise ValidationError("age", age, "должно быть целым числом")
    if age < 0 or age > 150:
        raise ValidationError("age", age, "должно быть от 0 до 150")
    return age

try:
    validate_age(-5)
except ValidationError as e:
    print(f"Ошибка: {e}")
    print(f"  Поле: {e.field}")
    print(f"  Значение: {e.value}")
```

---

## 🔹 Контекстные менеджеры (`with`)

```python
# Автоматически вызывает __enter__ при входе и __exit__ при выходе
with open("file.txt", "r") as f:
    data = f.read()
# Файл закрыт даже при исключении!

# Свой контекстный менеджер (класс)
class ManagedResource:
    def __enter__(self):
        print("Захват ресурса")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Освобождение ресурса")
        if exc_type:
            print(f"Произошла ошибка: {exc_val}")
        return False  # True = подавить исключение, False = пробросить

with ManagedResource() as r:
    print("Использование ресурса")
    # raise ValueError("Упс!")  # __exit__ всё равно вызовется!
```

```python
# Контекстный менеджер через генератор
from contextlib import contextmanager

@contextmanager
def managed_file(path, mode="r"):
    print(f"Открытие {path}")
    f = open(path, mode)
    try:
        yield f          # Передаём управление блоку with
    finally:
        print(f"Закрытие {path}")
        f.close()

with managed_file("test.txt", "w") as f:
    f.write("Данные")
```

---

## 🔹 Полезные исключения

| Исключение | Когда возникает |
|-----------|----------------|
| `ValueError` | Неправильное значение (напр., `int("abc")`) |
| `TypeError` | Неверный тип (напр., `"a" + 1`) |
| `KeyError` | Ключ не найден в словаре |
| `IndexError` | Индекс за пределами списка |
| `FileNotFoundError` | Файл не существует |
| `ZeroDivisionError` | Деление на ноль |
| `AttributeError` | Атрибут не существует |
| `ImportError` | Модуль не найден |
| `NotImplementedError` | Метод должен быть переопределён |

---

## 🔹 `traceback` — детальная информация

```python
import traceback
import sys

try:
    1 / 0
except ZeroDivisionError:
    # Вывести трейсбек
    traceback.print_exc()

    # Получить как строку
    tb_str = traceback.format_exc()

    # Доступ к объекту исключения
    exc_type, exc_value, exc_tb = sys.exc_info()
```

---

## 🔹 `warnings` — некритичные предупреждения

```python
import warnings

def old_function():
    warnings.warn("old_function устарела, используйте new_function",
                  DeprecationWarning, stacklevel=2)
    # Код выполняется дальше!

# Фильтрация
warnings.filterwarnings("ignore")           # Игнорировать все
warnings.filterwarnings("error")            # Превратить в исключения
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

---

## ⚠️ Антипаттерны

```python
# ❌ Пустой except (ловит ВСЁ, включая SystemExit и KeyboardInterrupt!)
try:
    risky_code()
except:
    pass  # Ошибка молча проглочена!

# ❌ Слишком широкий except
try:
    data = process()
except Exception:  # Ловит всё, маскирует баги
    pass

# ✅ Ловите только то, что ожидаете
try:
    data = process()
except ValueError:  # Только конкретная ошибка
    data = default

# ❌ Возврат из finally
def bad():
    try:
        return "try"
    finally:
        return "finally"  # Перезапишет return из try!
bad()  # "finally"
```

---

## 💡 Лучшие практики

1. **Ловите конкретные исключения**, а не `Exception` без надобности
2. **Не глотайте ошибки** — хотя бы логируйте их
3. **Пользовательские исключения** для бизнес-логики
4. **`finally` для очистки ресурсов** — закрытие файлов, соединений
5. **`with` всегда, когда возможно** — автоматическая очистка
6. **EAFP > LBYL**: "Easier to Ask Forgiveness than Permission" — проще попробовать и перехватить ошибку, чем проверять заранее

```python
# ❌ LBYL: Look Before You Leap
if "key" in d:
    value = d["key"]
else:
    value = default

# ✅ EAFP: Easier to Ask Forgiveness than Permission
try:
    value = d["key"]
except KeyError:
    value = default
```

---

## 🧪 Упражнения

1. Напишите функцию `safe_divide(a, b)`, возвращающую `Infinity` при делении на ноль
2. Создайте иерархию исключений для банковского приложения (InsufficientFundsError, InvalidPinError и т.д.)
3. Реализуйте контекстный менеджер `Timer`, измеряющий время выполнения блока
4. Напишите декоратор `@retry(max_attempts, exceptions)`, повторяющий функцию при указанных ошибках
