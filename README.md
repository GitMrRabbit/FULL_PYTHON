# 🐍 FULL_PYTHON — Полный курс Python с нуля до профессионала

## 👋 Для кого этот проект?

Для человека, который **вообще ничего не понимает** в программировании, но хочет стать
профессиональным Python-разработчиком или автоматизатором тестирования.

## 🗺️ КАК УЧИТЬСЯ? (Дорожная карта)

### Этап 1: Основы синтаксиса (2-3 недели)

Изучайте уроки **строго по порядку** — каждая тема опирается на предыдущую:

| Порядок | Урок | Что освоите |
|---------|------|------------|
| 1 | [`01_hello_world/`](python_basics/01_hello_world/) | Первая программа, `print()`, `input()` |
| 2 | [`02_variables_and_types/`](python_basics/02_variables_and_types/) | Переменные, типы `int`, `str`, `float`, `bool` |
| 3 | [`03_strings/`](python_basics/03_strings/) | Строки, срезы, методы |
| 4 | [`04_operators/`](python_basics/04_operators/) | `+`, `-`, `*`, `/`, `and`, `or`, `not` |
| 5 | [`05_conditions/`](python_basics/05_conditions/) | `if`, `elif`, `else`, `match/case` |
| 6 | [`06_loops/`](python_basics/06_loops/) | `for`, `while`, `range()`, `break`/`continue` |
| 7 | [`07_lists/`](python_basics/07_lists/) | Списки: добавление, удаление, срезы |
| 8 | [`08_tuples_sets/`](python_basics/08_tuples_sets/) | Кортежи и множества |
| 9 | [`09_dictionaries/`](python_basics/09_dictionaries/) | Словари `{ключ: значение}` |

### Этап 2: Функции и модули (1-2 недели)

| Порядок | Урок | Что освоите |
|---------|------|------------|
| 10 | [`10_functions/`](python_basics/10_functions/) | Создание функций, `def`, `return` |
| 11 | [`11_lambda_builtins/`](python_basics/11_lambda_builtins/) | `lambda`, `map`, `filter`, `sorted` |
| 12 | [`12_modules_packages/`](python_basics/12_modules_packages/) | Импорты, модули, `pip` |
| 13 | [`13_exceptions/`](python_basics/13_exceptions/) | Обработка ошибок, `try/except` |

### Этап 3: Работа с данными (1 неделя)

| Порядок | Урок | Что освоите |
|---------|------|------------|
| 14 | [`14_files/`](python_basics/14_files/) | Чтение/запись файлов, `pathlib`, JSON, CSV |
| 21 | [`21_comprehensions/`](python_basics/21_comprehensions/) | Генераторы списков/словарей/множеств |
| 22 | [`22_dates_and_times/`](python_basics/22_dates_and_times/) | Даты, время, `timedelta` |
| 23 | [`23_json_csv/`](python_basics/23_json_csv/) | JSON и CSV углублённо |
| 24 | [`24_regex/`](python_basics/24_regex/) | Регулярные выражения |

### Этап 4: ООП — Объектно-Ориентированное Программирование (2-3 недели)

| Порядок | Урок | Что освоите |
|---------|------|------------|
| 15 | [`15_oop_basics/`](python_basics/15_oop_basics/) | Классы, объекты, `__init__`, `self` |
| 16 | [`16_oop_inheritance/`](python_basics/16_oop_inheritance/) | Наследование, `super()`, полиморфизм |
| 17 | [`17_oop_magic_methods/`](python_basics/17_oop_magic_methods/) | `__str__`, `__len__`, `__call__`, `__iter__` |
| 18 | [`18_oop_properties/`](python_basics/18_oop_properties/) | `@property`, `@classmethod`, `@staticmethod` |

### Этап 5: Продвинутый Python (2 недели)

| Порядок | Урок | Что освоите |
|---------|------|------------|
| 19 | [`19_decorators/`](python_basics/19_decorators/) | Декораторы, `@wraps`, замыкания |
| 20 | [`20_generators_iterators/`](python_basics/20_generators_iterators/) | `yield`, итераторы, `itertools` |
| 25 | [`25_virtual_env/`](python_basics/25_virtual_env/) | Виртуальные окружения, `pip` |
| 26 | [`26_type_hints/`](python_basics/26_type_hints/) | Аннотации типов, `mypy` |

### Этап 6: Инструменты профессионала (2 недели)

| Порядок | Урок | Что освоите |
|---------|------|------------|
| 27 | [`27_testing_basics/`](python_basics/27_testing_basics/) | `pytest`, `unittest`, моки |
| 28 | [`28_concurrency/`](python_basics/28_concurrency/) | Потоки, процессы, `asyncio` |
| 29 | [`29_logging/`](python_basics/29_logging/) | Логирование, ротация, JSON-логи |

### Этап 7: Базы данных (1-2 недели)

| Порядок | Урок | Что освоите |
|---------|------|------------|
| 31 | [`31_sqlite/`](python_basics/31_sqlite/) | SQLite: таблицы, CRUD, JOIN |
| 32 | [`32_postgresql/`](python_basics/32_postgresql/) | PostgreSQL, `psycopg2`, JSONB |

### 🏆 Финал: Итоговый проект

| Порядок | Урок | Что освоите |
|---------|------|------------|
| 30 | [`30_final_project/`](python_basics/30_final_project/) | Консольное приложение «Менеджер задач» |

---

## 🧪 Бонус: Автоматизация тестирования

После освоения Python изучите:

| Порядок | Раздел | Что внутри |
|---------|--------|-----------|
| 1 | [`test_automation_framework/01_basics/`](test_automation_framework/01_basics/) | Основы pytest |
| 2 | [`test_automation_framework/02_intermediate/`](test_automation_framework/02_intermediate/) | Page Object, Selenium, DTO |
| 3 | [`test_automation_framework/03_professional/`](test_automation_framework/03_professional/) | API-тесты, Docker, Allure |

---

## 📖 КАК РАБОТАТЬ С КАЖДЫМ УРОКОМ?

1. **Прочитайте `README.md`** — там теория простыми словами
2. **Запустите `.py` файл** — посмотрите как код работает:
   ```bash
   python python_basics/01_hello_world/main.py
   ```
3. **Прочитайте комментарии в коде** — они объясняют КАЖДУЮ строку
4. **Сделайте упражнения** из раздела «Упражнения» в README.md
5. **Сверьтесь с ответами** в [`answers/`](python_basics/answers/) (решения всех упражнений)
6. **Экспериментируйте!** Меняйте код, ломайте, чините — только так учатся

---

## 📚 Вспомогательные материалы

| Файл | Что содержит |
|------|-------------|
| [`plans/master_plan.md`](plans/master_plan.md) | Полный план проекта |
| [`python_basics/GLOSSARY.md`](python_basics/GLOSSARY.md) | Словарь терминов |
| [`python_basics/CHEATSHEET.md`](python_basics/CHEATSHEET.md) | Шпаргалка по Python |
| [`python_basics/answers/`](python_basics/answers/) | Решения всех упражнений |

---

## ❓ Часто задаваемые вопросы

### «Я никогда не программировал(а). Смогу?»
**Да.** Начните с урока 01 и двигайтесь строго по порядку. Каждый урок объясняет
тему с нуля. Через 3-4 месяца регулярных занятий вы будете уверенно писать на Python.

### «Сколько времени займёт весь курс?»
При занятиях **1-2 часа в день** — около **3-4 месяцев** до уровня уверенного Junior.

### «Что делать если что-то непонятно?»
1. Перечитайте README.md урока
2. Запустите код и посмотрите что он делает
3. Поменяйте код и посмотрите что изменилось
4. Погуглите термин (например: «python list comprehension explained»)
5. Вернитесь к теме через пару дней — часто понимание приходит позже

### «Нужно ли учить всё подряд?»
Первые 14 уроков — **обязательно**. Остальное — в любом порядке, но
рекомендуемый путь указан в дорожной карте выше.

---

## 🎯 Цели по уровням

| Уровень | Уроки | Что вы умеете |
|---------|-------|--------------|
| 🔰 Начинающий | 01-09 | Писать простые скрипты, работать с данными |
| 🟡 Базовый | 10-14 | Создавать функции, читать/писать файлы |
| 🟠 Средний | 15-18, 21-26 | Объектно-ориентированный код, типизация |
| 🔴 Продвинутый | 19-20, 27-29 | Декораторы, генераторы, тесты, асинхронность |
| ⭐ Профи | 30-32 + Фреймворк | Полноценные приложения, БД, автотесты |

---

**Удачи в изучении Python! Главное — практика каждый день, даже по 30 минут.** 🚀
