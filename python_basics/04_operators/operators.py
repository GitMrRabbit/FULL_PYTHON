"""
УРОК 04: Операторы в Python
============================

Демонстрирует:
- Арифметические операторы (+, -, *, /, //, %, **)
- Операторы сравнения (==, !=, >, <, >=, <=)
- Логические операторы (and, or, not)
- Побитовые операторы (&, |, ^, ~, <<, >>)
- Операторы присваивания (=, +=, -= и т.д.)
- Операторы принадлежности (in, not in)
- Операторы идентичности (is, is not)
- Приоритет операторов
"""


def demo_arithmetic():
    """Арифметические операторы."""
    print("=" * 50)
    print("📌 АРИФМЕТИЧЕСКИЕ ОПЕРАТОРЫ")
    print("=" * 50)

    a, b = 10, 3

    print(f"a = {a}, b = {b}")
    print(f"a + b  = {a + b}    # сложение")
    print(f"a - b  = {a - b}     # вычитание")
    print(f"a * b  = {a * b}    # умножение")
    print(f"a / b  = {a / b}    # деление (всегда float!)")
    print(f"a // b = {a // b}    # целочисленное деление (floor division)")
    print(f"a % b  = {a % b}     # остаток от деления (modulo)")
    print(f"a ** b = {a ** b}   # возведение в степень")

    # Особенности деления
    print(f"\nОсобенности деления:")
    print(f"  10 / 3 = {10 / 3}      (всегда float)")
    print(f"  10 // 3 = {10 // 3}     (целая часть)")
    print(f"  -10 // 3 = {-10 // 3}   (округление ВНИЗ, к -∞)")
    print(f"  -10 % 3 = {-10 % 3}    (остаток всегда положительный)")

    # Приоритет: **, затем *, /, //, %, затем +, -
    print(f"\nПриоритет операторов:")
    print(f"  2 + 3 * 4 = {2 + 3 * 4}        # сначала умножение")
    print(f"  (2 + 3) * 4 = {(2 + 3) * 4}    # скобки меняют порядок")
    print(f"  2 ** 3 ** 2 = {2 ** 3 ** 2}    # правоассоциативно: 2**(3**2)=512")


def demo_comparison():
    """Операторы сравнения."""
    print("\n" + "=" * 50)
    print("📌 ОПЕРАТОРЫ СРАВНЕНИЯ")
    print("=" * 50)

    x, y = 5, 10

    print(f"x = {x}, y = {y}")
    print(f"x == y: {x == y}   # равно")
    print(f"x != y: {x != y}   # не равно")
    print(f"x > y:  {x > y}    # больше")
    print(f"x < y:  {x < y}    # меньше")
    print(f"x >= y: {x >= y}   # больше или равно")
    print(f"x <= y: {x <= y}   # меньше или равно")

    # Цепочки сравнений (уникальная фича Python!)
    print(f"\nЦепочки сравнений:")
    print(f"  1 < 2 < 3:  {1 < 2 < 3}     # True (1<2 И 2<3)")
    print(f"  1 < 2 > 3:  {1 < 2 > 3}     # False")
    print(f"  5 == 5 == 5: {5 == 5 == 5}   # True")
    print(f"  a < b < c эквивалентно a < b and b < c")

    # Сравнение строк (лексикографическое)
    print(f"\nСравнение строк:")
    print(f"  'apple' < 'banana': {'apple' < 'banana'}")
    print(f"  'A' < 'a': {'A' < 'a'}  (ASCII: A=65, a=97)")


def demo_logical():
    """Логические операторы: and, or, not."""
    print("\n" + "=" * 50)
    print("📌 ЛОГИЧЕСКИЕ ОПЕРАТОРЫ")
    print("=" * 50)

    # and: True если ОБА операнда True
    print("--- and (логическое И) ---")
    print(f"True and True:   {True and True}")
    print(f"True and False:  {True and False}")
    print(f"False and True:  {False and True}")
    print(f"False and False: {False and False}")

    # or: True если ХОТЯ БЫ ОДИН операнд True
    print("\n--- or (логическое ИЛИ) ---")
    print(f"True or True:   {True or True}")
    print(f"True or False:  {True or False}")
    print(f"False or True:  {False or True}")
    print(f"False or False: {False or False}")

    # not: инвертирует значение
    print("\n--- not (логическое НЕ) ---")
    print(f"not True:  {not True}")
    print(f"not False: {not False}")

    # Короткое замыкание (short-circuit evaluation)
    print("\n--- Короткое замыкание ---")
    # and: если первый False — второй НЕ вычисляется
    print(f"False and (1/0): {False and (1/0)}  # Нет ошибки! (1/0) не вычислялось")
    # or: если первый True — второй НЕ вычисляется
    print(f"True or (1/0): {True or (1/0)}      # Нет ошибки!")

    # Логические операторы возвращают ПОСЛЕДНИЙ вычисленный операнд!
    print(f"\nВозвращаемое значение:")
    print(f"  'hello' and 'world': {'hello' and 'world'}")  # 'world'
    print(f"  '' and 'world': {'""' and 'world'}")          # ''
    print(f"  'hello' or 'world': {'hello' or 'world'}")    # 'hello'
    print(f"  '' or 'world': {'""' or 'world'}")            # 'world'
    print(f"  '' or [] or 0 or 'last': {'""' or [] or 0 or 'last'}")  # 'last'


def demo_bitwise():
    """Побитовые операторы."""
    print("\n" + "=" * 50)
    print("📌 ПОБИТОВЫЕ ОПЕРАТОРЫ")
    print("=" * 50)

    a, b = 5, 3  # 5 = 0b0101, 3 = 0b0011

    print(f"a = {a} (0b{a:04b}), b = {b} (0b{b:04b})")
    print(f"a & b  = {a & b}  (0b{a & b:04b})   # побитовое И (AND)")
    print(f"a | b  = {a | b}  (0b{a | b:04b})   # побитовое ИЛИ (OR)")
    print(f"a ^ b  = {a ^ b}  (0b{a ^ b:04b})   # побитовое XOR")
    print(f"~a     = {~a}      # побитовое НЕ (NOT) — инвертирует все биты")
    print(f"a << 1 = {a << 1}  (0b{a << 1:04b})  # сдвиг влево (умножение на 2)")
    print(f"a >> 1 = {a >> 1}  (0b{a >> 1:04b})  # сдвиг вправо (деление на 2)")

    # Практическое применение
    print("\n--- Практические применения ---")
    # Проверка чётности
    print(f"  5 & 1 = {5 & 1}  (нечётное)")
    print(f"  4 & 1 = {4 & 1}  (чётное)")
    # Умножение/деление на 2
    print(f"  10 << 1 = {10 << 1}  (10 * 2)")
    print(f"  10 >> 1 = {10 >> 1}  (10 // 2)")
    # Проверка установленного бита (битовые флаги)
    READ, WRITE, EXECUTE = 0b100, 0b010, 0b001
    permissions = READ | WRITE  # 0b110
    print(f"  READ | WRITE = 0b{permissions:03b}")
    print(f"  Есть ли READ? {bool(permissions & READ)}")
    print(f"  Есть ли EXECUTE? {bool(permissions & EXECUTE)}")


def demo_assignment():
    """Операторы присваивания."""
    print("\n" + "=" * 50)
    print("📌 ОПЕРАТОРЫ ПРИСВАИВАНИЯ")
    print("=" * 50)

    x = 10
    print(f"x = 10  → x = {x}")

    x += 5   # x = x + 5
    print(f"x += 5  → x = {x}")

    x -= 3   # x = x - 3
    print(f"x -= 3  → x = {x}")

    x *= 2   # x = x * 2
    print(f"x *= 2  → x = {x}")

    x /= 4   # x = x / 4
    print(f"x /= 4  → x = {x}")

    x //= 2  # x = x // 2
    print(f"x //= 2 → x = {x}")

    x **= 3  # x = x ** 3
    print(f"x **= 3 → x = {x}")

    x %= 5   # x = x % 5
    print(f"x %= 5  → x = {x}")


def demo_membership_identity():
    """Операторы in, not in, is, is not."""
    print("\n" + "=" * 50)
    print("📌 ОПЕРАТОРЫ ПРИНАДЛЕЖНОСТИ И ИДЕНТИЧНОСТИ")
    print("=" * 50)

    # in / not in — проверка вхождения
    print("--- in / not in ---")
    fruits = ["яблоко", "банан", "вишня"]
    print(f"Список: {fruits}")
    print(f"'банан' in fruits: {'банан' in fruits}")
    print(f"'киви' in fruits: {'киви' in fruits}")
    print(f"'яблоко' not in fruits: {'яблоко' not in fruits}")

    # Работает и со строками
    print(f"  'ell' in 'hello': {'ell' in 'hello'}")
    print(f"  'x' in 'hello': {'x' in 'hello'}")

    # Работает со словарями (проверяет ключи)
    user = {"name": "Анна", "age": 25}
    print(f"  'name' in user: {'name' in user}")
    print(f"  'Анна' in user: {'Анна' in user}  # ищет по КЛЮЧАМ")

    # is / is not — проверка идентичности (один ли объект в памяти)
    print("\n--- is / is not ---")
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a

    print(f"a == b: {a == b}        # значения равны")
    print(f"a is b: {a is b}        # но это разные объекты")
    print(f"a is c: {a is c}        # c ссылается на тот же объект")
    print(f"a is not b: {a is not b}")

    # is None — стандартный паттерн
    value = None
    print(f"\nСтандартный паттерн: value is None = {value is None}")
    print(f"НИКОГДА не используйте value == None!")


def demo_priority():
    """Приоритет операторов."""
    print("\n" + "=" * 50)
    print("📌 ПРИОРИТЕТ ОПЕРАТОРОВ (от высшего к низшему)")
    print("=" * 50)

    # Таблица приоритетов (упрощённая)
    priorities = [
        ("()", "Скобки"),
        ("**", "Возведение в степень"),
        ("+x, -x, ~x", "Унарные плюс/минус, побитовое НЕ"),
        ("*, /, //, %", "Умножение, деление, остаток"),
        ("+, -", "Сложение, вычитание"),
        ("<<, >>", "Побитовые сдвиги"),
        ("&", "Побитовое И"),
        ("^", "Побитовое XOR"),
        ("|", "Побитовое ИЛИ"),
        ("==, !=, >, <, >=, <=, is, is not, in, not in", "Сравнения и проверки"),
        ("not", "Логическое НЕ"),
        ("and", "Логическое И"),
        ("or", "Логическое ИЛИ"),
    ]

    for op, desc in priorities:
        print(f"  {op:30} {desc}")

    print(f"\nПримеры:")
    print(f"  2 + 3 * 4 = {2 + 3 * 4}       # * приоритетнее +")
    print(f"  not True and False = {not True and False}  # not приоритетнее and")
    print(f"  not (True and False) = {not (True and False)}")


def main():
    """Главная функция."""
    print("🐍 УРОК 04: ОПЕРАТОРЫ В PYTHON")
    print("=" * 50)

    demo_arithmetic()
    demo_comparison()
    demo_logical()
    demo_bitwise()
    demo_assignment()
    demo_membership_identity()
    demo_priority()

    print("\n" + "=" * 50)
    print("✅ Урок 04 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. / всегда возвращает float, // — целочисленное деление")
    print("  2. Python поддерживает цепочки сравнений: 1 < x < 10")
    print("  3. Короткое замыкание: and/or не вычисляют правую часть без нужды")
    print("  4. Для проверки на None используйте `is None`, не `== None`")
    print("=" * 50)


if __name__ == "__main__":
    main()
