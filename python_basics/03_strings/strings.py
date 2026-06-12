"""
УРОК 03: Строки (str)
=====================

Этот файл демонстрирует:
- Создание строк разными способами
- Индексацию и срезы (slicing)
- Неизменяемость строк
- Escape-последовательности и raw-строки
- f-строки и форматирование
- Основные методы строк
- Конкатенацию, повторение, поиск подстрок
"""


def demo_creation():
    """Способы создания строк."""
    print("=" * 50)
    print("📌 СОЗДАНИЕ СТРОК")
    print("=" * 50)

    s1 = "Двойные кавычки"
    s2 = 'Одинарные кавычки'
    s3 = """Многострочная
строка через тройные кавычки"""
    s4 = str(42)       # из числа
    s5 = str(3.14)     # из float
    s6 = str(True)     # из bool ("True")

    print(f"s1: '{s1}'")
    print(f"s2: '{s2}'")
    print(f"s3: '{s3}'")
    print(f"s4: '{s4}'")
    print(f"s5: '{s5}'")
    print(f"s6: '{s6}'")

    # Кавычки внутри строк
    print(f"\nКавычки внутри строк:")
    print(f"  It's a nice day")         # двойные снаружи, одинарные внутри
    print(f'  Он сказал: "Привет!"')   # одинарные снаружи, двойные внутри
    print(f'  It\'s a nice day')        # экранирование \'


def demo_escape():
    """Escape-последовательности и raw-строки."""
    print("\n" + "=" * 50)
    print("📌 ESCAPE-ПОСЛЕДОВАТЕЛЬНОСТИ")
    print("=" * 50)

    print("Строка 1\\nСтрока 2 →")
    print("Строка 1\nСтрока 2")

    print("\nТабуляция \\t →")
    print("Имя:\tАнна\nВозраст:\t25")

    # Путь Windows (проблема!)
    bad_path = "C:\Users\admin\new_folder"  # \n и \a — escape!
    print(f"\n❌ Плохо (\\n стал переводом строки): {repr(bad_path)}")

    # Raw-строка: r"..." — отключает escape
    good_path = r"C:\Users\admin\new_folder"
    print(f"✅ Raw-строка: {good_path}")

    # Экранирование кавычек
    print(f"\nОн сказал: \"Python — это круто!\"")
    print(f'It\'s a wonderful day')

    # Unicode-символы
    print(f"\nUnicode: \\u2764 = \u2764")    # ❤
    print(f"Unicode: \\u2603 = \u2603")      # ☃
    print(f"Unicode: \\U0001F60A = \U0001F60A")  # 😊


def demo_indexing_slicing():
    """Индексация и срезы."""
    print("\n" + "=" * 50)
    print("📌 ИНДЕКСАЦИЯ И СРЕЗЫ")
    print("=" * 50)

    s = "Python"
    print(f"Строка: '{s}'")
    print(f"Индексы:   0    1    2    3    4    5")
    print(f"           P    y    t    h    o    n")
    print(f"Отрицательные: -6   -5   -4   -3   -2   -1")

    # Доступ по индексу
    print(f"\nДоступ по индексу:")
    print(f"  s[0] = '{s[0]}'")
    print(f"  s[1] = '{s[1]}'")
    print(f"  s[-1] = '{s[-1]}'  (последний)")
    print(f"  s[-2] = '{s[-2]}'  (предпоследний)")

    # Срезы [start:stop:step]
    print(f"\nСрезы:")
    print(f"  s[0:3]   = '{s[0:3]}'    (индексы 0,1,2)")
    print(f"  s[:3]    = '{s[:3]}'     (от начала до 2)")
    print(f"  s[3:]    = '{s[3:]}'     (с 3 до конца)")
    print(f"  s[::2]   = '{s[::2]}'    (каждый второй)")
    print(f"  s[1:5:2] = '{s[1:5:2]}'  (с 1 по 4, шаг 2)")
    print(f"  s[::-1]  = '{s[::-1]}'   (переворот!)")

    # Срез не вызывает ошибку при выходе за границы
    print(f"\n  s[0:100] = '{s[0:100]}'  (не ошибка!)")
    # s[100] — а вот так была бы IndexError!

    # Практические примеры срезов
    text = "Hello, World!"
    print(f"\nСтрока: '{text}'")
    print(f"  Первое слово: '{text[:5]}'")
    print(f"  Последние 6 символов: '{text[-6:]}'")
    print(f"  Без первого и последнего: '{text[1:-1]}'")
    print(f"  Каждый 3-й символ: '{text[::3]}'")


def demo_immutability():
    """Неизменяемость строк."""
    print("\n" + "=" * 50)
    print("📌 СТРОКИ НЕИЗМЕНЯЕМЫ (IMMUTABLE)")
    print("=" * 50)

    s = "hello"
    print(f"Исходная строка: '{s}'")

    # Строки нельзя изменить "на месте"
    try:
        s[0] = "H"
    except TypeError as e:
        print(f"❌ s[0] = 'H' → TypeError: {e}")

    # Правильный способ: создать новую строку
    s_new = "H" + s[1:]
    print(f"✅ Правильно: s_new = 'H' + s[1:] = '{s_new}'")

    # Исходная строка не изменилась
    print(f"Исходная строка всё ещё: '{s}'")


def demo_operations():
    """Конкатенация, повторение и другие операции."""
    print("\n" + "=" * 50)
    print("📌 ОПЕРАЦИИ СО СТРОКАМИ")
    print("=" * 50)

    # Конкатенация (склеивание)
    print(f"'Hello' + ' ' + 'World' = '{'Hello' + ' ' + 'World'}'")

    # Повторение
    print(f"'Ha' * 5 = '{'Ha' * 5}'")
    print(f"'-' * 30 = '{'-' * 30}'")

    # Проверка вхождения
    print(f"'ell' in 'hello' = {'ell' in 'hello'}")
    print(f"'xyz' in 'hello' = {'xyz' in 'hello'}")
    print(f"'ell' not in 'hello' = {'ell' not in 'hello'}")

    # Длина строки
    print(f"len('Python') = {len('Python')}")
    print(f"len('Привет') = {len('Привет')}")
    print(f"len('🐍') = {len('🐍')}")

    # Сравнение строк (лексикографическое)
    print(f"\nСравнение строк:")
    print(f"  'abc' < 'abd' = {'abc' < 'abd'}")
    print(f"  'A' < 'a' = {'A' < 'a'}  (заглавные МЕНЬШЕ строчных в ASCII)")
    print(f"  '2' < '10' = {'2' < '10'}  (сравнивается как строки, не числа!)")


def demo_f_strings():
    """f-строки и форматирование."""
    print("\n" + "=" * 50)
    print("📌 F-СТРОКИ")
    print("=" * 50)

    name = "Анна"
    age = 25
    pi = 3.141592653589793
    ratio = 0.856

    # Базовое использование
    print(f"Меня зовут {name}, мне {age} лет.")

    # Выражения внутри {}
    print(f"Через 10 лет будет {age + 10} лет.")
    print(f"Имя в верхнем регистре: {name.upper()}")

    # Форматирование чисел
    print(f"\nФорматирование чисел:")
    print(f"  π = {pi:.2f}")          # 2 знака после запятой
    print(f"  π = {pi:.4f}")          # 4 знака
    print(f"  Процент: {ratio:.1%}")   # 85.6%
    print(f"  Процент: {ratio:.2%}")   # 85.60%

    # Выравнивание и заполнение
    print(f"\nВыравнивание:")
    print(f"  |{name:<10}|  ← влево")
    print(f"  |{name:>10}|  ← вправо")
    print(f"  |{name:^10}|  ← по центру")
    print(f"  |{name:*^10}|  ← по центру, заполнение *")

    # Форматирование больших чисел
    big = 1234567890
    print(f"\nБольшие числа:")
    print(f"  {big:,}")       # 1,234,567,890
    print(f"  {big:_}")       # 1_234_567_890

    # Дата и время в f-строках
    from datetime import datetime
    now = datetime.now()
    print(f"\nДата и время:")
    print(f"  {now:%Y-%m-%d %H:%M:%S}")

    # Отладка: {var=} показывает имя переменной и значение
    print(f"\nОтладка с =:")
    print(f"  {name=}, {age=}, {pi=:.2f}")


def demo_methods():
    """Основные методы строк."""
    print("\n" + "=" * 50)
    print("📌 МЕТОДЫ СТРОК")
    print("=" * 50)

    s = "  Hello, World!  "

    # Регистр
    print("--- Регистр ---")
    print(f"  '{s}'.upper()      = '{s.upper()}'")
    print(f"  '{s}'.lower()      = '{s.lower()}'")
    print(f"  'hello world'.capitalize() = '{'hello world'.capitalize()}'")
    print(f"  'hello world'.title()     = '{'hello world'.title()}'")
    print(f"  'PyThOn'.swapcase()       = '{'PyThOn'.swapcase()}'")

    # Удаление пробелов
    print("\n--- Удаление пробелов ---")
    print(f"  '{s}'.strip()     = '{s.strip()}'")
    print(f"  '{s}'.lstrip()    = '{s.lstrip()}'")
    print(f"  '{s}'.rstrip()    = '{s.rstrip()}'")

    # Поиск и замена
    print("\n--- Поиск и замена ---")
    print(f"  'hello'.replace('l', 'X')     = '{'hello'.replace('l', 'X')}'")
    print(f"  'hello'.replace('l', 'X', 1)  = '{'hello'.replace('l', 'X', 1)}'")
    print(f"  'hello'.find('l')    = {'hello'.find('l')}")     # первый l
    print(f"  'hello'.rfind('l')   = {'hello'.rfind('l')}")    # последний l
    print(f"  'hello'.find('z')    = {'hello'.find('z')}")     # -1 (не найдено)
    print(f"  'hello'.index('l')   = {'hello'.index('l')}")    # ValueError если нет
    print(f"  'banana'.count('a')  = {'banana'.count('a')}")

    # Проверки
    print("\n--- Проверки ---")
    print(f"  'hello'.startswith('he') = {'hello'.startswith('he')}")
    print(f"  'hello'.endswith('lo')   = {'hello'.endswith('lo')}")
    print(f"  '123'.isdigit()    = {'123'.isdigit()}")
    print(f"  'abc'.isalpha()    = {'abc'.isalpha()}")
    print(f"  'abc123'.isalnum() = {'abc123'.isalnum()}")
    print(f"  '   '.isspace()    = {'   '.isspace()}")
    print(f"  'HELLO'.isupper()  = {'HELLO'.isupper()}")
    print(f"  'hello'.islower()  = {'hello'.islower()}")
    print(f"  'Hello World'.istitle() = {'Hello World'.istitle()}")

    # split и join
    print("\n--- split и join ---")
    data = "яблоко,банан,вишня"
    parts = data.split(",")
    print(f"  '{data}'.split(',') = {parts}")
    print(f"  ' - '.join({parts}) = '{' - '.join(parts)}'")

    # Разбиение с ограничением
    print(f"  'a,b,c,d'.split(',', 2) = {'a,b,c,d'.split(',', 2)}")

    # splitlines — разбиение по строкам
    multi = "строка1\nстрока2\nстрока3"
    print(f"  multi.splitlines() = {multi.splitlines()}")


def exercises():
    """Примеры решения упражнений из README.md."""
    print("\n" + "=" * 50)
    print("📌 РЕШЕНИЯ УПРАЖНЕНИЙ")
    print("=" * 50)

    # 1. Переворот строки
    def reverse_string(s):
        return s[::-1]

    print(f"reverse_string('Python') = '{reverse_string('Python')}'")

    # 2. Палиндром
    def is_palindrome(s):
        s = s.lower().replace(" ", "")  # Приводим к нижнему регистру, убираем пробелы
        return s == s[::-1]

    print(f"is_palindrome('А роза упала на лапу Азора') = "
          f"{is_palindrome('А роза упала на лапу Азора')}")
    print(f"is_palindrome('Python') = {is_palindrome('Python')}")

    # 3. Подсчёт гласных
    def count_vowels(s):
        vowels = "аеёиоуыэюяaeiou"
        return sum(1 for c in s.lower() if c in vowels)

    print(f"count_vowels('Привет, мир!') = {count_vowels('Привет, мир!')}")

    # 4. Разбор ФИО
    full_name = "Иванов Иван Иванович"
    surname, name, patronymic = full_name.split()
    print(f"Фамилия: {surname}, Имя: {name}, Отчество: {patronymic}")

    # 5. Удаление пробелов
    def remove_spaces(s):
        return s.replace(" ", "")

    print(f"remove_spaces('a b c d') = '{remove_spaces('a b c d')}'")


def main():
    """Главная функция."""
    print("🐍 УРОК 03: СТРОКИ (str)")
    print("=" * 50)

    demo_creation()
    demo_escape()
    demo_indexing_slicing()
    demo_immutability()
    demo_operations()
    demo_f_strings()
    demo_methods()
    exercises()

    print("\n" + "=" * 50)
    print("✅ Урок 03 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. Строки в Python НЕИЗМЕНЯЕМЫ (immutable)")
    print("  2. Срезы — мощнейший инструмент: s[start:stop:step]")
    print("  3. f-строки — современный способ форматирования")
    print("  4. Методы .split() и .join() — основные для разбора/сборки")
    print("=" * 50)


if __name__ == "__main__":
    main()
