"""
Урок 21: Comprehensions (Генераторы коллекций)
================================================

Темы:
  - List comprehensions [x for x in ...]
  - Dict comprehensions {k: v for k, v in ...}
  - Set comprehensions {x for x in ...}
  - Вложенные comprehensions
  - Comprehensions с условиями (if, if/else)
  - Generator expressions (x for x in ...)
"""

# =============================================================================
# 1. LIST COMPREHENSIONS
# =============================================================================

def list_comprehensions_demo():
    """Демонстрация list comprehensions."""
    print("=" * 60)
    print("1. LIST COMPREHENSIONS")
    print("=" * 60)

    # Базовая форма: [выражение for переменная in итерируемый]
    squares = [x ** 2 for x in range(10)]
    print(f"Квадраты: {squares}")

    # С условием (filter): [... for x in ... if условие]
    evens = [x for x in range(20) if x % 2 == 0]
    print(f"Чётные: {evens}")

    # С if/else (map): [... if условие else ... for x in ...]
    labels = ["чёт" if x % 2 == 0 else "нечет" for x in range(6)]
    print(f"Метки: {labels}")

    # Преобразование строк
    words = ["hello", "world", "python"]
    upper = [w.upper() for w in words]
    print(f"UPPER: {upper}")

    # Плоская карта (flat map)
    nested = [[1, 2], [3, 4], [5, 6]]
    flat = [item for sublist in nested for item in sublist]
    print(f"Flat: {flat}")

    # Вложенные циклы (декартово произведение)
    pairs = [(x, y) for x in range(3) for y in range(2)]
    print(f"Пары: {pairs}")

    # Comprehensions vs цикл — сравнение
    import timeit
    loop_time = timeit.timeit(
        "r=[]\nfor x in range(1000):\n  r.append(x*2)", number=1000
    )
    comp_time = timeit.timeit(
        "r=[x*2 for x in range(1000)]", number=1000
    )
    print(f"\nЦикл: {loop_time:.4f}с, Comprehension: {comp_time:.4f}с")
    print(f"Ускорение: {loop_time / comp_time:.1f}x")


# =============================================================================
# 2. DICT COMPREHENSIONS
# =============================================================================

def dict_comprehensions_demo():
    """Демонстрация dict comprehensions."""
    print("\n" + "=" * 60)
    print("2. DICT COMPREHENSIONS")
    print("=" * 60)

    # {ключ: значение for ... in ...}
    squares_dict = {x: x ** 2 for x in range(6)}
    print(f"Квадраты: {squares_dict}")

    # Из двух списков
    keys = ["a", "b", "c"]
    values = [1, 2, 3]
    merged = {k: v for k, v in zip(keys, values)}
    print(f"Из списков: {merged}")

    # С условием
    filtered = {k: v for k, v in squares_dict.items() if v > 10}
    print(f"v > 10: {filtered}")

    # Инвертирование словаря
    inverted = {v: k for k, v in merged.items()}
    print(f"Инвертированный: {inverted}")

    # Подсчёт частоты символов
    text = "abracadabra"
    freq = {ch: text.count(ch) for ch in set(text)}
    print(f"Частота букв: {freq}")

    # Вложенные словари
    matrix = {(i, j): i * j for i in range(3) for j in range(3)}
    print(f"Таблица умножения (3x3): {matrix}")


# =============================================================================
# 3. SET COMPREHENSIONS
# =============================================================================

def set_comprehensions_demo():
    """Демонстрация set comprehensions."""
    print("\n" + "=" * 60)
    print("3. SET COMPREHENSIONS")
    print("=" * 60)

    # Уникальные квадраты
    squares_set = {x ** 2 for x in range(-5, 6)}
    print(f"Квадраты: {squares_set}")

    # Удаление дубликатов с сохранением условия
    words = ["hello", "HELLO", "world", "WORLD", "Hello"]
    unique_lower = {w.lower() for w in words}
    print(f"Уникальные (lower): {unique_lower}")

    # Все буквы в тексте
    text = "Hello, World! Welcome to Python."
    letters = {ch.lower() for ch in text if ch.isalpha()}
    print(f"Буквы в тексте: {sorted(letters)}")


# =============================================================================
# 4. ВЛОЖЕННЫЕ COMPREHENSIONS
# =============================================================================

def matrix_transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Транспонирование матрицы через list comprehension."""
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def nested_comprehensions_demo():
    """Демонстрация вложенных comprehensions."""
    print("\n" + "=" * 60)
    print("4. ВЛОЖЕННЫЕ COMPREHENSIONS")
    print("=" * 60)

    # Матрица умножения
    mult_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
    print("Таблица умножения 5x5:")
    for row in mult_table:
        print(f"  {row}")

    # Транспонирование
    transposed = matrix_transpose(mult_table)
    print("\nТранспонированная:")
    for row in transposed:
        print(f"  {row}")

    # Список списков → плоский список
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [x for row in matrix for x in row]
    print(f"\nПлоский: {flat}")

    # Все делители чисел
    divisors = {n: [d for d in range(1, n + 1) if n % d == 0] for n in range(1, 11)}
    print(f"Делители: {divisors}")


# =============================================================================
# 5. ПРАКТИЧЕСКИЕ ПРИМЕРЫ
# =============================================================================

def practical_examples():
    """Практические примеры comprehensions."""
    print("\n" + "=" * 60)
    print("5. ПРАКТИЧЕСКИЕ ПРИМЕРЫ")
    print("=" * 60)

    # Фильтрация None
    data = [1, None, 2, None, 3, None, 4]
    clean = [x for x in data if x is not None]
    print(f"Без None: {clean}")

    # Парсинг строк
    csv_line = "Alice,30,Engineer\nBob,25,Designer"
    users = [
        {"name": name, "age": int(age), "role": role}
        for line in csv_line.strip().split("\n")
        for name, age, role in [line.split(",")]
    ]
    print(f"Пользователи из CSV: {users}")

    # Группировка по первой букве
    words = ["apple", "banana", "apricot", "blueberry", "avocado", "cherry"]
    grouped = {letter: [w for w in words if w.startswith(letter)]
               for letter in sorted(set(w[0] for w in words))}
    print(f"Группировка: {grouped}")

    # Все палиндромы в диапазоне
    start, end = 100, 300
    palindromes = [n for n in range(start, end + 1) if str(n) == str(n)[::-1]]
    print(f"Палиндромы {start}-{end}: {palindromes}")


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    list_comprehensions_demo()
    dict_comprehensions_demo()
    set_comprehensions_demo()
    nested_comprehensions_demo()
    practical_examples()

    print("\n" + "=" * 60)
    print("✅ УРОК 21 ЗАВЕРШЁН: COMPREHENSIONS ОСВОЕНЫ!")
    print("=" * 60)
