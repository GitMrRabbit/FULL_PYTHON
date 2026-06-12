# 📦 Урок 12: Модули и Пакеты в Python

## 📖 Теория

Модуль — это файл `.py`. Пакет — это директория с `__init__.py`. Модули позволяют организовать код, переиспользовать его и подключать библиотеки.

---

## 🔹 Импорт модулей

```python
# Базовые способы
import math                     # Импорт модуля целиком
from math import sqrt, ceil     # Импорт конкретных функций
from math import *              # Импорт ВСЕГО (НЕ рекомендуется!)
import math as m                # Псевдоним
from pathlib import Path        # Импорт класса

# Использование
math.sqrt(16)    # 4.0
sqrt(16)         # 4.0 (при from import)
m.sqrt(16)       # 4.0 (при import as)
```

---

## 🔹 Создание своего модуля

**`my_utils.py`:**
```python
"""Модуль с полезными функциями."""

__version__ = "1.0.0"
__all__ = ["add", "multiply"]  # Контролирует from module import *

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def _private_helper():  # По соглашению: _ = private
    pass

# Код ниже выполняется только при прямом запуске
if __name__ == "__main__":
    print("Этот код НЕ выполнится при импорте")
```

**Использование:**
```python
import my_utils
my_utils.add(3, 4)  # 7
```

---

## 🔹 `if __name__ == "__main__"`

```python
# module.py
def main():
    print("Запуск как программа")

if __name__ == "__main__":
    main()  # Выполнится только при: python module.py
    # НЕ выполнится при: import module
```

---

## 🔹 Пакеты (packages)

```
my_package/
├── __init__.py          # Пакетный инициализатор
├── core.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── api/
    ├── __init__.py
    └── client.py
```

**`__init__.py`:**
```python
# Можно импортировать для удобства пользователей пакета
from .core import main_function
from .utils.helpers import helper

__all__ = ["main_function", "helper"]

# Версия пакета
__version__ = "1.0.0"
```

**Импорт из пакета:**
```python
import my_package
from my_package import main_function
from my_package.utils.helpers import helper
from my_package import *  # Только то, что в __all__
```

---

## 🔹 Относительные импорты

```python
# Внутри my_package/utils/helpers.py
from . import something          # Текущая директория
from .. import core              # Родительская директория
from ..api import client         # Соседняя директория
from ..api.client import Client  # Конкретный класс
```

⚠️ Относительные импорты работают **только внутри пакетов!**

---

## 🔹 Стандартная библиотека Python

### Часто используемые модули:

| Модуль | Назначение |
|--------|-----------|
| `os` | Операционная система, переменные окружения |
| `sys` | Системные функции, аргументы командной строки |
| `math` | Математические функции |
| `random` | Генерация случайных чисел |
| `datetime` | Работа с датами и временем |
| `json` | Сериализация в JSON |
| `csv` | Чтение/запись CSV |
| `re` | Регулярные выражения |
| `collections` | Продвинутые контейнеры (Counter, defaultdict, deque) |
| `itertools` | Итераторы (combinations, permutations, chain) |
| `pathlib` | Современная работа с путями |
| `logging` | Логирование |
| `argparse` | Парсинг аргументов командной строки |
| `venv` | Виртуальные окружения |
| `unittest` | Модульное тестирование |

---

## 🔹 `pip` — менеджер пакетов

```bash
pip install requests           # Установить пакет
pip install requests==2.28.0   # Конкретная версия
pip install "requests>=2.20"   # Минимальная версия
pip install -r requirements.txt # Из файла
pip uninstall requests          # Удалить
pip list                        # Список установленных пакетов
pip freeze > requirements.txt   # Сохранить зависимости
pip show requests               # Информация о пакете
```

**`requirements.txt`:**
```
requests==2.28.0
pytest>=7.0.0
selenium~=4.4.0  # Совместимая версия (4.4.x)
```

---

## 🔹 Виртуальное окружение (venv)

```bash
# Создание
python -m venv venv

# Активация
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Деактивация
deactivate
```

---

## 🔹 `importlib` — продвинутые импорты

```python
import importlib

# Динамический импорт
module_name = "json"
json_module = importlib.import_module(module_name)

# Перезагрузка модуля (полезно при разработке)
importlib.reload(my_module)
```

---

## ⚠️ Частые ошибки

```python
# ❌ Циклический импорт
# a.py: from b import func_b
# b.py: from a import func_a  # ImportError!

# ❌ Конфликт имён с модулем
# Не называйте свой файл math.py, json.py и т.д.!

# ❌ from module import *
# Загрязняет пространство имён, трудно отследить происхождение

# ❌ Запуск пакета как скрипта
# python my_package/utils/helpers.py  # Относительные импорты сломаются!
# python -m my_package.utils.helpers  # ✅ Правильно
```

---

## 🧪 Упражнения

1. Создайте пакет `calculator` с модулями `basic.py` и `scientific.py`
2. Напишите скрипт, который динамически импортирует модуль по имени из аргументов командной строки
3. Создайте `setup.py` или `pyproject.toml` для вашего пакета
4. Изучите структуру любого популярного пакета (requests, flask, pytest)
