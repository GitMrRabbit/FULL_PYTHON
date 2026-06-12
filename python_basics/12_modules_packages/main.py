"""
УРОК 12: Модули и пакеты
=========================

Демонстрирует:
- Импорт модулей: import, from ... import, import ... as
- if __name__ == "__main__"
- Создание пакетов (__init__.py)
- Стандартная библиотека: math, random, datetime, os, sys
- Установка сторонних пакетов через pip
"""


def demo_import_styles():
    """Разные способы импорта."""
    print("=" * 50)
    print("📌 СПОСОБЫ ИМПОРТА")
    print("=" * 50)

    # 1. import module — импорт всего модуля
    import math
    print(f"math.sqrt(16) = {math.sqrt(16)}")
    print(f"math.pi = {math.pi}")

    # 2. from module import name — импорт конкретного имени
    from math import sin, cos, radians
    angle = radians(90)
    print(f"\nsin(90°) = {sin(angle):.1f}")
    print(f"cos(90°) = {cos(angle):.1f}")

    # 3. from module import * — импорт ВСЕХ имён (НЕ РЕКОМЕНДУЕТСЯ!)
    # from math import *  # загрязняет пространство имён

    # 4. import module as alias — псевдоним
    import numpy as np  # (если установлен)
    # print(np.array([1, 2, 3]))

    # 5. from module import name as alias
    from math import factorial as fact
    print(f"\nfactorial(5) = {fact(5)}")


def demo_name_main():
    """Конструкция if __name__ == '__main__'."""
    print("\n" + "=" * 50)
    print("📌 if __name__ == '__main__'")
    print("=" * 50)

    print(f"__name__ текущего файла: '{__name__}'")

    # Импортируем наш демо-модуль
    import my_module
    print(f"\nИмпортирован модуль: {my_module.MODULE_NAME}")
    print(f"Версия: {my_module.MODULE_VERSION}")
    print(f"my_module.greet('Мир'): {my_module.greet('Мир')}")

    # Объяснение:
    # - При прямом запуске файла __name__ == "__main__"
    # - При импорте __name__ == имя модуля
    # - Это позволяет писать код, который работает и как модуль, и как скрипт


def demo_stdlib():
    """Обзор полезных модулей стандартной библиотеки."""
    print("\n" + "=" * 50)
    print("📌 СТАНДАРТНАЯ БИБЛИОТЕКА")
    print("=" * 50)

    # os — работа с операционной системой
    import os
    print(f"os.name = '{os.name}'")
    print(f"os.getcwd() = '{os.getcwd()}'")
    print(f"os.path.join('a', 'b', 'c') = '{os.path.join('a', 'b', 'c')}'")

    # sys — системные параметры
    import sys
    print(f"\nsys.version = '{sys.version[:30]}...'")
    print(f"sys.platform = '{sys.platform}'")
    print(f"sys.path (первые 2): {[p[:40] for p in sys.path[:2]]}")

    # random — генерация случайных чисел
    import random
    print(f"\nrandom.randint(1, 100) = {random.randint(1, 100)}")
    print(f"random.random() = {random.random():.3f}")  # от 0 до 1
    print(f"random.choice([1,2,3,4,5]) = {random.choice([1, 2, 3, 4, 5])}")

    items = [1, 2, 3, 4, 5]
    random.shuffle(items)
    print(f"random.shuffle: {items}")

    # datetime — работа с датой и временем
    from datetime import datetime, timedelta
    now = datetime.now()
    print(f"\nСейчас: {now:%Y-%m-%d %H:%M:%S}")
    print(f"Через неделю: {(now + timedelta(days=7)):%Y-%m-%d}")

    # collections — дополнительные коллекции
    from collections import Counter, defaultdict, namedtuple
    counter = Counter("abracadabra")
    print(f"\nCounter('abracadabra'): {counter}")
    print(f"Топ-2: {counter.most_common(2)}")

    # itertools — инструменты для итераций
    from itertools import combinations, permutations
    print(f"\ncombinations('ABC', 2): {list(combinations('ABC', 2))}")
    print(f"permutations('ABC', 2): {list(permutations('ABC', 2))}")

    # functools — инструменты для функций
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def fib(n):
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    print(f"\nФибоначчи с кэшем: fib(20) = {fib(20)}")
    print(f"Инфо кэша: {fib.cache_info()}")


def demo_packages():
    """Создание и использование пакетов."""
    print("\n" + "=" * 50)
    print("📌 ПАКЕТЫ")
    print("=" * 50)

    print("""
Структура пакета:

my_package/
├── __init__.py      # Делает директорию пакетом
├── module_a.py      # Модуль A
├── module_b.py      # Модуль B
└── subpackage/
    ├── __init__.py
    └── module_c.py  # Модуль C

Использование:
    import my_package.module_a
    from my_package.subpackage import module_c
    from my_package.module_a import some_function
""")


def demo_pip():
    """pip — установка сторонних пакетов."""
    print("=" * 50)
    print("📌 PIP — МЕНЕДЖЕР ПАКЕТОВ")
    print("=" * 50)

    print("""
Основные команды pip:

    pip install package_name        # Установить пакет
    pip install package==1.0.0      # Установить конкретную версию
    pip install -r requirements.txt # Установить все из файла
    pip uninstall package_name      # Удалить пакет
    pip list                        # Показать установленные пакеты
    pip freeze > requirements.txt   # Сохранить список зависимостей
    pip show package_name           # Информация о пакете

Популярные пакеты:
    requests    — HTTP-запросы
    pytest      — Тестирование
    numpy       — Научные вычисления
    pandas      — Анализ данных
    selenium    — Автоматизация браузера
    flask       — Веб-фреймворк
    django      — Веб-фреймворк
    sqlalchemy  — ORM для БД
    pydantic    — Валидация данных
    black       — Форматирование кода
    pylint      — Линтер
""")


def main():
    """Главная функция."""
    print("🐍 УРОК 12: МОДУЛИ И ПАКЕТЫ")
    print("=" * 50)
    print(f"Этот файл запущен как: __name__ = '{__name__}'")

    demo_import_styles()
    demo_name_main()
    demo_stdlib()
    demo_packages()
    demo_pip()

    print("\n" + "=" * 50)
    print("✅ Урок 12 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. import module / from module import name / import module as alias")
    print("  2. if __name__ == '__main__' — код только при прямом запуске")
    print("  3. Стандартная библиотека огромна: os, sys, math, random, json, collections...")
    print("  4. Пакет = директория с __init__.py")
    print("  5. pip — установка сторонних библиотек")
    print("=" * 50)


if __name__ == "__main__":
    main()
