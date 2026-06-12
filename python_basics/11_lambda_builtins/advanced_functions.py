"""
УРОК 11: lambda, map, filter, reduce и другие встроенные функции
==================================================================

Демонстрирует:
- lambda — анонимные функции
- map() — применение функции к каждому элементу
- filter() — фильтрация по условию
- reduce() — свёртка последовательности
- sorted(), min(), max() с key
- any(), all(), zip(), enumerate() (повторение + углубление)
"""


def demo_lambda():
    """Анонимные функции (lambda)."""
    print("=" * 50)
    print("📌 LAMBDA-ФУНКЦИИ")
    print("=" * 50)

    # Синтаксис: lambda аргументы: выражение
    # lambda — это функция БЕЗ имени, которая возвращает результат выражения

    # Обычная функция
    def add(a, b):
        return a + b

    # То же самое через lambda
    add_lambda = lambda a, b: a + b

    print(f"add(3, 5) = {add(3, 5)}")
    print(f"add_lambda(3, 5) = {add_lambda(3, 5)}")

    # lambda может принимать любое количество аргументов
    square = lambda x: x ** 2
    is_even = lambda x: x % 2 == 0
    get_full_name = lambda first, last: f"{first} {last}"

    print(f"square(7) = {square(7)}")
    print(f"is_even(4) = {is_even(4)}")
    print(f"get_full_name('Иван', 'Петров') = {get_full_name('Иван', 'Петров')}")

    # lambda часто используется там, где нужна одноразовая функция
    # Например, сортировка по ключу:
    students = [
        {"name": "Анна", "grade": 85},
        {"name": "Борис", "grade": 92},
        {"name": "Виктор", "grade": 78},
    ]

    # Сортировка по полю grade
    sorted_students = sorted(students, key=lambda s: s["grade"])
    print(f"\nСортировка по grade: {[s['name'] for s in sorted_students]}")

    # Обратная сортировка
    sorted_desc = sorted(students, key=lambda s: s["grade"], reverse=True)
    print(f"Обратная: {[s['name'] for s in sorted_desc]}")

    # lambda с условием (тернарный оператор)
    absolute = lambda x: x if x >= 0 else -x
    print(f"\nabsolute(-5) = {absolute(-5)}")

    # НЕ злоупотребляйте lambda! Если логика сложная — пишите обычную функцию.
    # ❌ Плохо: lambda x: ... (10 строк выражения)
    # ✅ Хорошо: def complex_function(x): ...


def demo_map():
    """map() — применение функции к каждому элементу."""
    print("\n" + "=" * 50)
    print("📌 map()")
    print("=" * 50)

    # map(func, iterable) — применяет func к каждому элементу
    numbers = [1, 2, 3, 4, 5]

    # Возведение в квадрат
    squares = list(map(lambda x: x ** 2, numbers))
    print(f"Квадраты: {squares}")

    # Преобразование типов
    str_nums = ["1", "2", "3", "4", "5"]
    int_nums = list(map(int, str_nums))
    print(f"map(int, {str_nums}) = {int_nums}")

    # map с несколькими итерируемыми объектами
    a = [1, 2, 3]
    b = [10, 20, 30]
    summed = list(map(lambda x, y: x + y, a, b))
    print(f"Поэлементная сумма: {summed}")

    # Практический пример: нормализация строк
    names = ["  анна  ", "БОРИС", "  Виктор  "]
    cleaned = list(map(lambda s: s.strip().capitalize(), names))
    print(f"Очистка имён: {cleaned}")

    # map возвращает ИТЕРАТОР (ленивый)
    # Его нужно "потребить" через list() или цикл
    mapped = map(lambda x: x * 2, range(1000000))
    print(f"\nmap НЕ вычисляет сразу! Это итератор: {type(mapped).__name__}")
    print(f"Первые 5: {list(mapped)[:5]}")

    # Альтернатива: list comprehension (часто читаемее)
    squares_lc = [x ** 2 for x in numbers]
    print(f"\nList comprehension (альтернатива map): {squares_lc}")


def demo_filter():
    """filter() — фильтрация элементов по условию."""
    print("\n" + "=" * 50)
    print("📌 filter()")
    print("=" * 50)

    numbers = range(20)

    # Чётные числа
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Чётные: {evens}")

    # Положительные числа
    mixed = [-3, -1, 0, 2, 4, -5, 7]
    positive = list(filter(lambda x: x > 0, mixed))
    print(f"Положительные: {positive}")

    # filter с None — убирает falsy-значения
    items = [0, 1, "", "hello", None, [], [1, 2], False, True, {}, {"a": 1}]
    truthy = list(filter(None, items))
    print(f"\nfilter(None) — убирает falsy:")
    print(f"  Исходные: {items}")
    print(f"  Truthy:   {truthy}")

    # Практический пример: фильтрация словаря
    users = [
        {"name": "Анна", "age": 25, "active": True},
        {"name": "Борис", "age": 17, "active": True},
        {"name": "Виктор", "age": 30, "active": False},
        {"name": "Галина", "age": 22, "active": True},
    ]

    # Активные совершеннолетние пользователи
    active_adults = list(filter(
        lambda u: u["active"] and u["age"] >= 18,
        users
    ))
    print(f"\nАктивные совершеннолетние: {[u['name'] for u in active_adults]}")

    # Альтернатива: list comprehension
    active_adults_lc = [u for u in users if u["active"] and u["age"] >= 18]
    print(f"То же через LC: {[u['name'] for u in active_adults_lc]}")


def demo_reduce():
    """reduce() — свёртка последовательности."""
    print("\n" + "=" * 50)
    print("📌 reduce()")
    print("=" * 50)

    from functools import reduce

    # reduce(func, iterable, [initial]) — последовательно применяет func
    # reduce(lambda x, y: ..., [a, b, c, d])
    # = func(func(func(a, b), c), d)

    numbers = [1, 2, 3, 4, 5]

    # Сумма всех чисел
    total = reduce(lambda x, y: x + y, numbers)
    print(f"Сумма {numbers} = {total}")
    print(f"  По шагам: (1+2)=3, (3+3)=6, (6+4)=10, (10+5)=15")

    # Произведение (аналог math.prod)
    product = reduce(lambda x, y: x * y, numbers)
    print(f"Произведение: {product}")

    # Максимум (аналог max)
    max_val = reduce(lambda x, y: x if x > y else y, numbers)
    print(f"Максимум: {max_val}")

    # С начальным значением
    total_with_initial = reduce(lambda x, y: x + y, numbers, 100)
    print(f"Сумма с initial=100: {total_with_initial}")

    # Практический пример: объединение словарей
    dicts = [{"a": 1}, {"b": 2}, {"c": 3}]
    merged = reduce(lambda x, y: {**x, **y}, dicts)
    print(f"\nОбъединение словарей: {merged}")

    # Практический пример: построение цепочки вызовов
    def compose(*functions):
        """Композиция функций: compose(f, g, h)(x) = f(g(h(x)))."""
        return reduce(lambda f, g: lambda x: f(g(x)), functions)

    add_one = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x ** 2

    pipeline = compose(square, double, add_one)
    # (5 + 1) = 6, * 2 = 12, ** 2 = 144
    print(f"\ncompose(square, double, add_one)(5) = {pipeline(5)}")


def demo_builtins():
    """sorted, min, max, any, all с key."""
    print("\n" + "=" * 50)
    print("📌 sorted, min, max, any, all С key")
    print("=" * 50)

    # sorted() — возвращает новый отсортированный список
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"sorted: {sorted(nums)}")
    print(f"sorted reverse: {sorted(nums, reverse=True)}")

    # sorted с key
    words = ["яблоко", "банан", "киви", "апельсин", "груша"]
    by_length = sorted(words, key=len)
    print(f"\nПо длине: {by_length}")
    by_last_char = sorted(words, key=lambda w: w[-1])
    print(f"По последней букве: {by_last_char}")

    # min / max с key
    print(f"\nmin по длине: {min(words, key=len)}")
    print(f"max по длине: {max(words, key=len)}")

    # any() — True если хотя бы один True
    print(f"\nany([False, False, True]): {any([False, False, True])}")
    print(f"any([False, False, False]): {any([False, False, False])}")

    # all() — True если ВСЕ True
    print(f"all([True, True, True]): {all([True, True, True])}")
    print(f"all([True, False, True]): {all([True, False, True])}")

    # Практическое применение
    numbers = [2, 4, 6, 8]
    print(f"\nall чётные? {all(n % 2 == 0 for n in numbers)}")
    print(f"any > 5? {any(n > 5 for n in numbers)}")

    # Проверка пароля
    def is_strong_password(pwd):
        return all([
            len(pwd) >= 8,
            any(c.isupper() for c in pwd),
            any(c.islower() for c in pwd),
            any(c.isdigit() for c in pwd),
        ])

    print(f"\nis_strong_password('abc'): {is_strong_password('abc')}")
    print(f"is_strong_password('Abc12345'): {is_strong_password('Abc12345')}")


def main():
    """Главная функция."""
    print("🐍 УРОК 11: LAMBDA, MAP, FILTER, REDUCE")
    print("=" * 50)

    demo_lambda()
    demo_map()
    demo_filter()
    demo_reduce()
    demo_builtins()

    print("\n" + "=" * 50)
    print("✅ Урок 11 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. lambda — одноразовая анонимная функция")
    print("  2. map(func, iter) — применить функцию к каждому элементу")
    print("  3. filter(func, iter) — оставить только подходящие элементы")
    print("  4. reduce(func, iter) — свернуть последовательность в одно значение")
    print("  5. list comprehensions часто читаемее, чем map/filter")
    print("=" * 50)


if __name__ == "__main__":
    main()
