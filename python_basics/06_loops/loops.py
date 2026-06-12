"""
УРОК 06: Циклы (for, while)
============================

Демонстрирует:
- Цикл for: итерация по спискам, строкам, словарям, range()
- Цикл while: условие продолжения
- break — досрочный выход из цикла
- continue — пропуск текущей итерации
- pass — пустой блок
- for/else и while/else — блок после успешного завершения цикла
- enumerate() — индекс + значение
- zip() — параллельная итерация
- Вложенные циклы
"""


def demo_for_loop():
    """Цикл for: итерация по коллекциям."""
    print("=" * 50)
    print("📌 ЦИКЛ for")
    print("=" * 50)

    # Итерация по списку
    print("--- Итерация по списку ---")
    fruits = ["яблоко", "банан", "вишня", "апельсин"]
    for fruit in fruits:
        print(f"  Фрукт: {fruit}")

    # Итерация по строке (по символам)
    print("\n--- Итерация по строке ---")
    word = "Python"
    for char in word:
        print(f"  Символ: {char}")

    # Итерация по словарю
    print("\n--- Итерация по словарю ---")
    user = {"name": "Анна", "age": 25, "city": "Москва"}

    print("  Ключи (по умолчанию):")
    for key in user:
        print(f"    {key}")

    print("  Ключи явно:")
    for key in user.keys():
        print(f"    {key}")

    print("  Значения:")
    for value in user.values():
        print(f"    {value}")

    print("  Ключ + Значение:")
    for key, value in user.items():
        print(f"    {key}: {value}")

    # Итерация по множеству
    print("\n--- Итерация по множеству ---")
    numbers = {1, 2, 3, 4, 5}
    for n in numbers:
        print(f"  {n}", end=" ")
    print("(порядок не гарантирован!)")


def demo_range():
    """Функция range() — генератор числовых последовательностей."""
    print("\n" + "=" * 50)
    print("📌 RANGE()")
    print("=" * 50)

    # range(stop) — от 0 до stop-1
    print("range(5):", list(range(5)))

    # range(start, stop) — от start до stop-1
    print("range(2, 7):", list(range(2, 7)))

    # range(start, stop, step) — с шагом
    print("range(0, 10, 2):", list(range(0, 10, 2)))
    print("range(10, 0, -1):", list(range(10, 0, -1)))  # обратный порядок

    # Практическое применение
    print("\nТаблица умножения на 7:")
    for i in range(1, 11):
        print(f"  7 × {i:2} = {7 * i:2}")

    # range() — это не список, а ленивый объект! Экономит память.
    r = range(1_000_000)
    print(f"\nrange(1_000_000) занимает {r.__sizeof__()} байт")
    print(f"list(range(1_000_000)) занял бы ~8 МБ!")


def demo_while():
    """Цикл while."""
    print("\n" + "=" * 50)
    print("📌 ЦИКЛ while")
    print("=" * 50)

    # Простой while
    count = 1
    while count <= 5:
        print(f"  Итерация {count}")
        count += 1

    # while True — бесконечный цикл с условием выхода
    print("\nПоиск первого числа > 100, делящегося на 17:")
    n = 100
    while True:
        n += 1
        if n % 17 == 0:
            print(f"  Найдено: {n}")
            break

    # while с проверкой ввода
    print("\n--- while для ввода (пример логики) ---")
    # В реальном коде:
    # while True:
    #     answer = input("Введите 'exit' для выхода: ")
    #     if answer == "exit":
    #         break
    print("  (пример интерактивного ввода — запустите код чтобы попробовать)")


def demo_break_continue_pass():
    """break, continue, pass."""
    print("\n" + "=" * 50)
    print("📌 break, continue, pass")
    print("=" * 50)

    # break — немедленный выход из цикла
    print("--- break ---")
    for i in range(10):
        if i == 5:
            print(f"  break на i={i}")
            break
        print(f"  i = {i}")

    # continue — пропустить остаток итерации, перейти к следующей
    print("\n--- continue ---")
    for i in range(10):
        if i % 2 == 0:  # чётные пропускаем
            continue
        print(f"  Нечётное: {i}")

    # pass — ничего не делает (заглушка)
    print("\n--- pass ---")
    for i in range(3):
        if i == 1:
            pass  # TODO: добавить логику позже
            print(f"  i={i}: pass (заглушка)")
        else:
            print(f"  i={i}: обычная итерация")


def demo_loop_else():
    """for/else и while/else — уникальная фича Python!"""
    print("\n" + "=" * 50)
    print("📌 for/else и while/else")
    print("=" * 50)

    # else выполняется, если цикл завершился ЕСТЕСТВЕННО (без break)
    print("--- for/else (без break) ---")
    for i in range(3):
        print(f"  i = {i}")
    else:
        print("  ✅ Цикл завершился естественно — else выполнен!")

    print("\n--- for/else (с break) ---")
    for i in range(5):
        print(f"  i = {i}")
        if i == 2:
            print("  💥 break!")
            break
    else:
        print("  Это сообщение НЕ появится")

    # Практический пример: поиск элемента
    def find_prime(numbers):
        """Ищет первое простое число в списке."""
        for n in numbers:
            if n > 1 and all(n % i != 0 for i in range(2, int(n ** 0.5) + 1)):
                print(f"  Найдено простое число: {n}")
                break
        else:
            print("  Простых чисел не найдено!")

    find_prime([4, 6, 8, 10, 12])  # нет простых
    find_prime([4, 6, 7, 8, 10])   # 7 — простое


def demo_enumerate_zip():
    """enumerate() и zip() — вспомогательные функции для циклов."""
    print("\n" + "=" * 50)
    print("📌 enumerate() и zip()")
    print("=" * 50)

    # enumerate() — получаем индекс и значение одновременно
    print("--- enumerate() ---")
    fruits = ["яблоко", "банан", "вишня"]

    # Без enumerate (ручной счётчик)
    print("  Без enumerate:")
    idx = 0
    for fruit in fruits:
        print(f"    {idx}: {fruit}")
        idx += 1

    # С enumerate (красиво!)
    print("  С enumerate:")
    for idx, fruit in enumerate(fruits):
        print(f"    {idx}: {fruit}")

    # enumerate с начальным индексом
    print("  enumerate с start=1:")
    for idx, fruit in enumerate(fruits, start=1):
        print(f"    {idx}. {fruit}")

    # zip() — параллельная итерация по нескольким коллекциям
    print("\n--- zip() ---")
    names = ["Анна", "Борис", "Виктор"]
    ages = [25, 30, 35]
    cities = ["Москва", "Питер", "Казань"]

    for name, age, city in zip(names, ages, cities):
        print(f"  {name}, {age} лет, {city}")

    # Разная длина — zip остановится на самой короткой
    print("\n  Разная длина коллекций (zip — по короткой):")
    short = [1, 2]
    long = [10, 20, 30, 40]
    for a, b in zip(short, long):
        print(f"    {a} — {b}")

    # zip_longest — по самой длинной (заполняет None)
    from itertools import zip_longest
    print("  zip_longest (по длинной, заполняет None):")
    for a, b in zip_longest(short, long):
        print(f"    {a} — {b}")


def demo_nested_loops():
    """Вложенные циклы."""
    print("\n" + "=" * 50)
    print("📌 ВЛОЖЕННЫЕ ЦИКЛЫ")
    print("=" * 50)

    # Таблица умножения
    print("Таблица умножения 5×5:")
    print("    ", end="")
    for j in range(1, 6):
        print(f"{j:4}", end="")
    print("\n   " + "-" * 20)

    for i in range(1, 6):
        print(f"{i:2} |", end="")
        for j in range(1, 6):
            print(f"{i * j:4}", end="")
        print()

    # Генерация всех комбинаций
    print("\nВсе комбинации двух кубиков:")
    combos = []
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            combos.append((d1, d2))
    print(f"  Всего комбинаций: {len(combos)}")
    print(f"  Первые 5: {combos[:5]}")


def demo_list_comprehension_intro():
    """Краткое введение в list comprehensions."""
    print("\n" + "=" * 50)
    print("📌 КРАТКО: LIST COMPREHENSIONS (подробнее в уроке 21)")
    print("=" * 50)

    # Вместо:
    squares = []
    for i in range(10):
        squares.append(i ** 2)
    print(f"Обычный цикл: {squares}")

    # Можно написать:
    squares = [i ** 2 for i in range(10)]
    print(f"Comprehension: {squares}")

    # С условием
    evens = [i for i in range(20) if i % 2 == 0]
    print(f"Чётные: {evens}")

    # Словарь
    word = "hello"
    char_count = {c: word.count(c) for c in set(word)}
    print(f"Подсчёт символов: {char_count}")


def main():
    """Главная функция."""
    print("🐍 УРОК 06: ЦИКЛЫ")
    print("=" * 50)

    demo_for_loop()
    demo_range()
    demo_while()
    demo_break_continue_pass()
    demo_loop_else()
    demo_enumerate_zip()
    demo_nested_loops()
    demo_list_comprehension_intro()

    print("\n" + "=" * 50)
    print("✅ Урок 06 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. for — итерация по любым коллекциям (списки, строки, словари)")
    print("  2. range() — ленивый генератор чисел, экономит память")
    print("  3. break — выход, continue — пропуск, pass — заглушка")
    print("  4. for/else — уникально: else выполняется после успешного цикла")
    print("  5. enumerate() и zip() — мощные помощники для циклов")
    print("=" * 50)


if __name__ == "__main__":
    main()
