"""
Демонстрационный модуль для урока 12.

Показывает:
- Как создавать модули
- Переменные уровня модуля
- Функции для экспорта
- Конструкцию if __name__ == "__main__"
"""

# Переменные уровня модуля (доступны при импорте)
MODULE_NAME = "my_module"
MODULE_VERSION = "1.0.0"
__all__ = ["greet", "add", "PI", "MODULE_NAME"]  # что экспортируется при from module import *

# Константа
PI = 3.14159


def greet(name):
    """Приветствует пользователя."""
    return f"Привет, {name} из модуля {MODULE_NAME}!"


def add(a, b):
    """Складывает два числа."""
    return a + b


def _private_function():
    """Приватная функция (соглашение: _ в начале имени).
    
    Не будет экспортирована при `from module import *`.
    Но технически всё ещё доступна при явном импорте.
    """
    return "Я приватная функция"


# Код ниже выполнится ТОЛЬКО при прямом запуске файла
if __name__ == "__main__":
    print(f"Модуль {MODULE_NAME} v{MODULE_VERSION} запущен напрямую!")
    print(greet("Анна"))
    print(f"2 + 3 = {add(2, 3)}")
    print(f"PI = {PI}")
    print(f"_private_function(): {_private_function()}")
else:
    print(f"Модуль {MODULE_NAME} импортирован!")
