"""
УРОК 02: Переменные и типы данных
===================================

Этот файл демонстрирует:
- Создание переменных и присваивание значений
- Все основные типы данных: int, float, str, bool, NoneType
- Функцию type() для определения типа
- Приведение (конвертацию) типов
- Множественное присваивание
- Особенности типов int и float
- Логические значения и truthy/falsy
"""


def demo_variables():
    """Создание и использование переменных."""
    print("=" * 50)
    print("📌 ПЕРЕМЕННЫЕ И ПРИСВАИВАНИЕ")
    print("=" * 50)

    # Переменные создаются в момент первого присваивания
    name = "Алексей"        # str
    age = 30                # int
    height = 1.82           # float
    is_student = False      # bool
    nothing = None          # NoneType

    print(f"name = {name} (тип: {type(name).__name__})")
    print(f"age = {age} (тип: {type(age).__name__})")
    print(f"height = {height} (тип: {type(height).__name__})")
    print(f"is_student = {is_student} (тип: {type(is_student).__name__})")
    print(f"nothing = {nothing} (тип: {type(nothing).__name__})")

    # Python — динамическая типизация: переменная может менять тип
    x = 42
    print(f"\nСначала x = {x} (тип: {type(x).__name__})")
    x = "теперь я строка"
    print(f"Потом x = {x} (тип: {type(x).__name__})")

    # Множественное присваивание
    a, b, c = 1, 2, 3
    print(f"\nМножественное присваивание: a={a}, b={b}, c={c}")

    # Обмен значений без временной переменной (swap)
    a, b = b, a
    print(f"После swap: a={a}, b={b}")

    # Одно значение — нескольким переменным
    x = y = z = 0
    print(f"x={x}, y={y}, z={z}")

    # Распаковка (unpacking)
    numbers = [10, 20, 30]
    first, second, third = numbers
    print(f"Распаковка списка: {first}, {second}, {third}")


def demo_types():
    """Подробный разбор всех типов данных."""
    print("\n" + "=" * 50)
    print("📌 ПОДРОБНЫЙ РАЗБОР ТИПОВ ДАННЫХ")
    print("=" * 50)

    # === INT: целые числа ===
    print("\n--- Целые числа (int) ---")
    print(f"Обычное: {42}")
    print(f"Отрицательное: {-7}")
    print(f"Огромное (2^100): {2 ** 100}")  # Python поддерживает сколь угодно большие целые!
    print(f"Двоичное 0b1010 = {0b1010}")
    print(f"Восьмеричное 0o12 = {0o12}")
    print(f"Шестнадцатеричное 0xA = {0xA}")

    # Функции преобразования систем счисления
    print(f"bin(10) = {bin(10)}")    # '0b1010'
    print(f"oct(10) = {oct(10)}")    # '0o12'
    print(f"hex(10) = {hex(10)}")    # '0xa'

    # === FLOAT: числа с плавающей точкой ===
    print("\n--- Дробные числа (float) ---")
    print(f"Обычное: {3.14}")
    print(f"Экспоненциальная запись: 1e-5 = {1e-5}")  # 0.00001

    # ВАЖНО: Проблема точности float
    print(f"\n⚠️ Проблема точности float:")
    print(f"0.1 + 0.2 = {0.1 + 0.2}")  # 0.30000000000000004
    print(f"0.1 + 0.2 == 0.3: {0.1 + 0.2 == 0.3}")  # False!

    # Решение — модуль decimal
    from decimal import Decimal
    print(f"Decimal('0.1') + Decimal('0.2') = {Decimal('0.1') + Decimal('0.2')}")
    print(f"Decimal('0.1') + Decimal('0.2') == Decimal('0.3'): "
          f"{Decimal('0.1') + Decimal('0.2') == Decimal('0.3')}")

    # Специальные значения float
    print(f"\nСпециальные значения:")
    print(f"float('inf') = {float('inf')}")
    print(f"float('-inf') = {float('-inf')}")
    print(f"float('nan') = {float('nan')}")
    print(f"float('inf') > 999999999: {float('inf') > 999999999}")

    # === STR: строки ===
    print("\n--- Строки (str) ---")
    s1 = "Двойные кавычки"
    s2 = 'Одинарные кавычки'
    s3 = """Тройные кавычки
позволяют писать
многострочный текст"""
    s4 = "Строка с 'кавычками' внутри"
    print(f"s1: {s1}")
    print(f"s2: {s2}")
    print(f"s3: {s3}")
    print(f"s4: {s4}")

    # === BOOL: логический тип ===
    print("\n--- Логический тип (bool) ---")
    print(f"True: {True}, тип: {type(True).__name__}")
    print(f"False: {False}, тип: {type(False).__name__}")

    # bool — подкласс int!
    print(f"True == 1: {True == 1}")
    print(f"False == 0: {False == 0}")
    print(f"True + True + False = {True + True + False}")  # 2

    # Что считается False (Falsy-значения)
    print(f"\nFalsy-значения (bool(x) == False):")
    print(f"  bool(0) = {bool(0)}")
    print(f"  bool(0.0) = {bool(0.0)}")
    print(f"  bool('') = {bool('')}")
    print(f"  bool([]) = {bool([])}")
    print(f"  bool({{}}) = {bool({})}")
    print(f"  bool(None) = {bool(None)}")
    print(f"  bool(set()) = {bool(set())}")

    # Всё остальное — True
    print(f"\nTruthy-значения (bool(x) == True):")
    print(f"  bool(42) = {bool(42)}")
    print(f"  bool(-1) = {bool(-1)}")
    print(f"  bool('hello') = {bool('hello')}")
    print(f"  bool([1, 2]) = {bool([1, 2])}")


def demo_type_conversion():
    """Приведение (конвертация) типов."""
    print("\n" + "=" * 50)
    print("📌 ПРИВЕДЕНИЕ ТИПОВ")
    print("=" * 50)

    # Строка в число
    print(f"int('123') = {int('123')}")
    print(f"float('3.14') = {float('3.14')}")

    # Число в строку
    print(f"str(42) = '{str(42)}'")
    print(f"str(3.14) = '{str(3.14)}'")

    # В bool
    print(f"bool(1) = {bool(1)}")
    print(f"bool(0) = {bool(0)}")
    print(f"bool('hello') = {bool('hello')}")
    print(f"bool('') = {bool('')}")

    # В список/кортеж из строки
    print(f"list('abc') = {list('abc')}")
    print(f"tuple('abc') = {tuple('abc')}")

    # Внимание: не всё можно привести!
    print("\n⚠️ Ошибки при приведении:")
    try:
        int("abc123")
    except ValueError as e:
        print(f"  int('abc123') → ValueError: {e}")

    try:
        int("3.14")  # Нельзя строку с точкой в int
    except ValueError as e:
        print(f"  int('3.14') → ValueError: {e}")
        print(f"  Правильно: int(float('3.14')) = {int(float('3.14'))}")


def demo_identity():
    """id(), is, == — идентичность и равенство."""
    print("\n" + "=" * 50)
    print("📌 ИДЕНТИЧНОСТЬ И РАВЕНСТВО (id, is, ==)")
    print("=" * 50)

    # id() возвращает адрес объекта в памяти
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a

    print(f"a = {a}, id = {id(a)}")
    print(f"b = {b}, id = {id(b)}")
    print(f"c = {c}, id = {id(c)}")

    # == проверяет равенство ЗНАЧЕНИЙ
    print(f"\na == b: {a == b}")  # True — значения равны

    # is проверяет, что это ОДИН И ТОТ ЖЕ объект в памяти
    print(f"a is b: {a is b}")    # False — разные объекты
    print(f"a is c: {a is c}")    # True — c ссылается на тот же объект

    # Integer caching: Python кэширует маленькие целые числа (-5 до 256)
    x = 256
    y = 256
    print(f"\n256 is 256: {x is y}")  # True (кэшированы)

    x = 257
    y = 257
    print(f"257 is 257: {x is y}")   # False (обычно, зависит от реализации)

    # isinstance() — проверка принадлежности типу
    print(f"\nisinstance(42, int): {isinstance(42, int)}")
    print(f"isinstance(3.14, (int, float)): {isinstance(3.14, (int, float))}")
    print(f"isinstance('hello', str): {isinstance('hello', str)}")


def demo_naming():
    """Правила именования переменных."""
    print("\n" + "=" * 50)
    print("📌 ИМЕНОВАНИЕ ПЕРЕМЕННЫХ (PEP 8)")
    print("=" * 50)

    # snake_case — для переменных и функций
    user_name = "Иван"
    total_price = 1499.99
    max_retry_count = 3

    # UPPER_CASE — для констант
    PI = 3.14159
    MAX_CONNECTIONS = 100
    DEFAULT_TIMEOUT = 30

    # _ в начале — "приватная" переменная (соглашение)
    _internal = "не используй меня снаружи модуля"

    # _ — переменная-заглушка (когда значение не нужно)
    first, _, third = (1, 2, 3)  # 2 пропускаем

    print(f"snake_case: {user_name}, {total_price}, {max_retry_count}")
    print(f"CONSTANTS: PI={PI}, MAX_CONNECTIONS={MAX_CONNECTIONS}")
    print(f"_internal: {_internal}")
    print(f"first={first}, third={third} (пропустили _ = {_})")


def main():
    """Главная функция."""
    print("🐍 УРОК 02: ПЕРЕМЕННЫЕ И ТИПЫ ДАННЫХ")
    print("=" * 50)

    demo_variables()
    demo_types()
    demo_type_conversion()
    demo_identity()
    demo_naming()

    print("\n" + "=" * 50)
    print("✅ Урок 02 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. Python — динамически типизированный язык")
    print("  2. Основные типы: int, float, str, bool, NoneType")
    print("  3. type() — узнать тип, isinstance() — проверить тип")
    print("  4. bool — подкласс int, True==1, False==0")
    print("  5. float имеет ограниченную точность (используйте Decimal)")
    print("=" * 50)


if __name__ == "__main__":
    main()
