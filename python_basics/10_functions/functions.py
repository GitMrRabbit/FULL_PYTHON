"""
УРОК 10: Функции (def)
=======================

Демонстрирует:
- Создание функций: def, return, docstring
- Аргументы: позиционные, именованные, значения по умолчанию
- *args (произвольное количество позиционных аргументов)
- **kwargs (произвольное количество именованных аргументов)
- Области видимости: local, enclosing, global, built-in (LEGB)
- Рекурсия — функция вызывает саму себя
- Аннотации типов (кратко, подробнее в уроке 26)
"""


def demo_basics():
    """Создание и вызов функций."""
    print("=" * 50)
    print("📌 ФУНКЦИИ — ОСНОВЫ")
    print("=" * 50)

    # Простейшая функция
    def greet():
        """Просто приветствует пользователя."""  # docstring
        print("Привет, Мир!")

    greet()
    print(f"docstring: {greet.__doc__}")

    # Функция с параметрами
    def greet_person(name, greeting="Привет"):
        """Приветствует человека по имени."""
        return f"{greeting}, {name}!"

    print(f"\ngreet_person('Анна'): {greet_person('Анна')}")
    print(f"greet_person('Борис', 'Здравствуй'): {greet_person('Борис', 'Здравствуй')}")

    # Именованные аргументы (keyword arguments)
    print(f"greet_person(greeting='Хай', name='Виктор'): "
          f"{greet_person(greeting='Хай', name='Виктор')}")

    # return — возврат значения. Без return функция возвращает None
    def no_return():
        x = 42  # ничего не возвращает

    result = no_return()
    print(f"\nФункция без return возвращает: {result}")


def demo_args_types():
    """Типы аргументов функций."""
    print("\n" + "=" * 50)
    print("📌 ТИПЫ АРГУМЕНТОВ")
    print("=" * 50)

    # 1. Позиционные (обязательные)
    # 2. Со значениями по умолчанию (необязательные)
    # 3. *args — переменное число позиционных
    # 4. **kwargs — переменное число именованных
    # 5. Keyword-only (после *)
    # 6. Positional-only (до /)

    def full_demo(a, b, c=10, *args, d, e=20, **kwargs):
        """
        a, b      — обязательные позиционные
        c=10      — с значением по умолчанию
        *args     — оставшиеся позиционные собираются в кортеж
        d         — keyword-only (обязательный именованный!)
        e=20      — keyword-only с значением по умолчанию
        **kwargs  — оставшиеся именованные собираются в словарь
        """
        print(f"  a={a}, b={b}, c={c}")
        print(f"  args={args}")
        print(f"  d={d}, e={e}")
        print(f"  kwargs={kwargs}")

    print("Вызов full_demo(1, 2, 3, 4, 5, d=6, f=7, g=8):")
    full_demo(1, 2, 3, 4, 5, d=6, f=7, g=8)


def demo_star_args():
    """*args и **kwargs подробно."""
    print("\n" + "=" * 50)
    print("📌 *args И **kwargs")
    print("=" * 50)

    # *args — собирает позиционные аргументы в кортеж
    def sum_all(*args):
        """Суммирует все переданные числа."""
        print(f"  args = {args}, сумма = {sum(args)}")
        return sum(args)

    sum_all(1, 2, 3)
    sum_all(10, 20, 30, 40, 50)

    # **kwargs — собирает именованные аргументы в словарь
    def print_info(**kwargs):
        """Выводит все переданные именованные аргументы."""
        for key, value in kwargs.items():
            print(f"  {key}: {value}")

    print("\nprint_info(name='Анна', age=25, city='Москва'):")
    print_info(name="Анна", age=25, city="Москва")

    # Распаковка (unpacking) при вызове
    def multiply(a, b, c):
        return a * b * c

    numbers = [2, 3, 4]
    print(f"\nmultiply(*[2, 3, 4]) = {multiply(*numbers)}")

    kwargs_dict = {"a": 2, "b": 3, "c": 4}
    print(f"multiply(**{{'a':2,'b':3,'c':4}}) = {multiply(**kwargs_dict)}")

    # Универсальная функция-обёртка
    def logger(func):
        """Декоратор-заглушка (подробнее в уроке 19)."""
        def wrapper(*args, **kwargs):
            print(f"  Вызов {func.__name__}({args}, {kwargs})")
            result = func(*args, **kwargs)
            print(f"  Результат: {result}")
            return result
        return wrapper

    @logger
    def add(a, b):
        return a + b

    add(5, 7)


def demo_scope():
    """Области видимости (LEGB)."""
    print("\n" + "=" * 50)
    print("📌 ОБЛАСТИ ВИДИМОСТИ (LEGB)")
    print("=" * 50)

    # L - Local (локальная — внутри функции)
    # E - Enclosing (внешняя — во внешней функции)
    # G - Global (глобальная — на уровне модуля)
    # B - Built-in (встроенная — встроенные имена Python)

    # Глобальная переменная
    global_var = "Я глобальная"

    def outer():
        enclosing_var = "Я из внешней функции"

        def inner():
            local_var = "Я локальная"
            print(f"  inner видит: {local_var}")
            print(f"  inner видит: {enclosing_var}")
            print(f"  inner видит: {global_var}")
            return local_var

        inner()
        # print(local_var)  # Ошибка! local_var не видна здесь

    outer()

    # global — изменить глобальную переменную
    counter = 0

    def increment():
        global counter  # без global будет создана локальная переменная!
        counter += 1

    increment()
    increment()
    print(f"\ncounter после двух increment(): {counter}")

    # nonlocal — изменить переменную из внешней функции
    def outer2():
        x = 10

        def inner():
            nonlocal x  # без nonlocal нельзя изменить x из outer2
            x += 5
            print(f"  inner: x = {x}")

        print(f"  outer до inner: x = {x}")
        inner()
        print(f"  outer после inner: x = {x}")

    outer2()


def demo_recursion():
    """Рекурсия — функция вызывает саму себя."""
    print("\n" + "=" * 50)
    print("📌 РЕКУРСИЯ")
    print("=" * 50)

    # Факториал: n! = n * (n-1)!
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    for i in range(6):
        print(f"  factorial({i}) = {factorial(i)}")

    # Числа Фибоначчи: F(n) = F(n-1) + F(n-2)
    def fibonacci(n, memo=None):
        """Числа Фибоначчи с мемоизацией (кэшированием)."""
        if memo is None:
            memo = {}
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
        return memo[n]

    print(f"\n  fibonacci(10) = {fibonacci(10)}")
    print(f"  fibonacci(30) = {fibonacci(30)}")

    # Обход вложенных структур
    def deep_flatten(lst):
        """Рекурсивно разворачивает вложенные списки."""
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(deep_flatten(item))
            else:
                result.append(item)
        return result

    nested = [1, [2, [3, 4], 5], 6]
    print(f"\n  deep_flatten({nested}) = {deep_flatten(nested)}")

    # Внимание: глубокая рекурсия приведёт к RecursionError!
    print(f"  Максимальная глубина рекурсии: {__import__('sys').getrecursionlimit()}")


def demo_advanced():
    """Продвинутые темы функций."""
    print("\n" + "=" * 50)
    print("📌 ПРОДВИНУТЫЕ ТЕМЫ")
    print("=" * 50)

    # Функции — объекты первого класса
    # Их можно присваивать переменным, передавать как аргументы, возвращать из функций

    def square(x):
        return x ** 2

    def cube(x):
        return x ** 3

    # Функция как аргумент
    def apply(func, values):
        return [func(v) for v in values]

    nums = [1, 2, 3, 4, 5]
    print(f"apply(square, {nums}) = {apply(square, nums)}")
    print(f"apply(cube, {nums}) = {apply(cube, nums)}")

    # Функция, возвращающая функцию
    def power_factory(exponent):
        def power(base):
            return base ** exponent
        return power

    square2 = power_factory(2)
    cube2 = power_factory(3)
    print(f"\npower_factory(2)(5) = {power_factory(2)(5)}")
    print(f"square2(5) = {square2(5)}")
    print(f"cube2(5) = {cube2(5)}")

    # lambda — анонимная функция (подробнее в уроке 11)
    sorted_by_second = sorted(
        [(1, 3), (2, 2), (3, 1)],
        key=lambda x: x[1]
    )
    print(f"\nsorted с lambda: {sorted_by_second}")


def main():
    """Главная функция."""
    print("🐍 УРОК 10: ФУНКЦИИ")
    print("=" * 50)

    demo_basics()
    demo_args_types()
    demo_star_args()
    demo_scope()
    demo_recursion()
    demo_advanced()

    print("\n" + "=" * 50)
    print("✅ Урок 10 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. def создаёт функцию, return возвращает значение")
    print("  2. *args собирает позиционные аргументы, **kwargs — именованные")
    print("  3. LEGB — порядок поиска имён: Local → Enclosing → Global → Built-in")
    print("  4. global / nonlocal — для изменения переменных из внешних областей")
    print("  5. Функции — объекты первого класса: можно передавать и возвращать")
    print("=" * 50)


if __name__ == "__main__":
    main()
