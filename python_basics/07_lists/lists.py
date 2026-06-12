"""
УРОК 07: Списки (list)
=======================

Демонстрирует:
- Создание списков разными способами
- Индексация и срезы (как у строк)
- Основные методы: append, extend, insert, remove, pop, index, count, sort, reverse, clear, copy
- Многомерные списки (матрицы)
- Копирование: поверхностное (shallow) и глубокое (deep)
- Стеки и очереди на списках
"""


def demo_creation():
    """Создание списков."""
    print("=" * 50)
    print("📌 СОЗДАНИЕ СПИСКОВ")
    print("=" * 50)

    # Пустой список
    empty1 = []
    empty2 = list()
    print(f"Пустой: {empty1}, {empty2}")

    # С элементами
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True, None, [1, 2]]
    print(f"Числа: {numbers}")
    print(f"Смешанный: {mixed}")

    # Из других коллекций
    chars = list("Python")  # из строки
    print(f"list('Python') = {chars}")

    from_tuple = list((1, 2, 3))  # из кортежа
    print(f"list((1,2,3)) = {from_tuple}")

    from_range = list(range(5))  # из range
    print(f"list(range(5)) = {from_range}")

    # Генератор списка (list comprehension)
    squares = [x ** 2 for x in range(10)]
    print(f"Квадраты: {squares}")

    # Повторение
    zeros = [0] * 5
    print(f"[0] * 5 = {zeros}")
    print(f"⚠️ Осторожно: [[0]*3]*3 создаёт ссылки на один и тот же список!")

    bad_matrix = [[0] * 3] * 3
    print(f"  {bad_matrix}")
    bad_matrix[0][0] = 99
    print(f"  После bad_matrix[0][0] = 99: {bad_matrix} (изменились все строки!)")


def demo_indexing_slicing():
    """Индексация и срезы (аналогично строкам)."""
    print("\n" + "=" * 50)
    print("📌 ИНДЕКСАЦИЯ И СРЕЗЫ")
    print("=" * 50)

    lst = [10, 20, 30, 40, 50, 60]
    print(f"Список: {lst}")

    print(f"lst[0] = {lst[0]}")
    print(f"lst[-1] = {lst[-1]} (последний)")
    print(f"lst[1:4] = {lst[1:4]}")
    print(f"lst[:3] = {lst[:3]}")
    print(f"lst[3:] = {lst[3:]}")
    print(f"lst[::2] = {lst[::2]} (каждый второй)")
    print(f"lst[::-1] = {lst[::-1]} (переворот)")

    # В ОТЛИЧИЕ от строк, списки можно ИЗМЕНЯТЬ через срезы!
    lst[1:3] = [200, 300]  # Замена элементов
    print(f"\nlst[1:3] = [200, 300] → {lst}")

    lst[1:3] = [999]  # Замена двух элементов одним
    print(f"lst[1:3] = [999] → {lst}")


def demo_methods():
    """Основные методы списков."""
    print("\n" + "=" * 50)
    print("📌 МЕТОДЫ СПИСКОВ")
    print("=" * 50)

    # append — добавить в конец
    fruits = ["яблоко", "банан"]
    fruits.append("вишня")
    print(f"append: {fruits}")

    # extend — добавить все элементы из другой коллекции
    fruits.extend(["апельсин", "киви"])
    print(f"extend: {fruits}")

    # insert — вставить по индексу
    fruits.insert(1, "манго")  # на позицию 1
    print(f"insert(1, 'манго'): {fruits}")

    # remove — удалить первое вхождение по значению
    fruits.remove("банан")
    print(f"remove('банан'): {fruits}")

    # pop — удалить и вернуть элемент по индексу (по умолчанию последний)
    last = fruits.pop()
    print(f"pop() → '{last}', осталось: {fruits}")

    second = fruits.pop(1)  # удалить по индексу
    print(f"pop(1) → '{second}', осталось: {fruits}")

    # index — найти индекс элемента
    idx = fruits.index("вишня")
    print(f"index('вишня') = {idx}")

    # count — количество вхождений
    fruits.append("яблоко")
    print(f"count('яблоко') = {fruits.count('яблоко')}")

    # sort — сортировка на месте
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    nums.sort()
    print(f"\nsort(): {nums}")
    nums.sort(reverse=True)
    print(f"sort(reverse=True): {nums}")

    # sorted() — возвращает новый отсортированный список
    original = [3, 1, 2]
    sorted_list = sorted(original)
    print(f"sorted({original}) = {sorted_list}, original всё ещё {original}")

    # reverse — перевернуть на месте
    nums.reverse()
    print(f"reverse(): {nums}")

    # clear — очистить список
    temp = [1, 2, 3]
    temp.clear()
    print(f"clear(): {temp}")

    # copy — поверхностная копия
    a = [1, 2, [3, 4]]
    b = a.copy()
    print(f"\ncopy(): a={a}, b={b}")


def demo_copy():
    """Поверхностное и глубокое копирование."""
    print("\n" + "=" * 50)
    print("📌 КОПИРОВАНИЕ: SHALLOW vs DEEP")
    print("=" * 50)

    import copy

    original = [1, 2, [10, 20], 3]

    # Поверхностная копия (shallow)
    # Способы сделать shallow copy:
    shallow1 = original.copy()
    shallow2 = original[:]
    shallow3 = list(original)

    # Глубокая копия (deep)
    deep = copy.deepcopy(original)

    print(f"original:  {original}")
    print(f"shallow:   {shallow1}")
    print(f"deep:      {deep}")

    # Изменяем вложенный список в оригинале
    original[2][0] = 999
    print(f"\nПосле original[2][0] = 999:")
    print(f"original:  {original}")
    print(f"shallow:   {shallow1}  ← ИЗМЕНИЛСЯ! (ссылка на тот же вложенный список)")
    print(f"deep:      {deep}      ← НЕ изменился (полная копия)")

    # Проверка идентичности
    print(f"\noriginal is shallow: {original is shallow1}")  # False
    print(f"original[2] is shallow[2]: {original[2] is shallow1[2]}")  # True!
    print(f"original[2] is deep[2]: {original[2] is deep[2]}")  # False


def demo_stack_queue():
    """Стек и очередь на списках."""
    print("\n" + "=" * 50)
    print("📌 СТЕК И ОЧЕРЕДЬ")
    print("=" * 50)

    # Стек (LIFO — Last In, First Out)
    print("--- Стек (через append/pop) ---")
    stack = []
    stack.append("A")
    stack.append("B")
    stack.append("C")
    print(f"После добавления: {stack}")
    print(f"pop() → {stack.pop()}")
    print(f"pop() → {stack.pop()}")
    print(f"Осталось: {stack}")

    # Очередь (FIFO — First In, First Out)
    print("\n--- Очередь (через collections.deque) ---")
    from collections import deque
    queue = deque()
    queue.append("Клиент 1")
    queue.append("Клиент 2")
    queue.append("Клиент 3")
    print(f"Очередь: {list(queue)}")
    print(f"Обслуживаем: {queue.popleft()}")
    print(f"Обслуживаем: {queue.popleft()}")
    print(f"Осталось: {list(queue)}")

    # Почему deque, а не list для очереди?
    # list.pop(0) — O(n), deque.popleft() — O(1)!


def demo_multidimensional():
    """Многомерные списки (матрицы)."""
    print("\n" + "=" * 50)
    print("📌 МНОГОМЕРНЫЕ СПИСКИ (МАТРИЦЫ)")
    print("=" * 50)

    # Создание матрицы 3×3
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    print("Матрица 3×3:")
    for row in matrix:
        print(f"  {row}")

    # Доступ к элементу
    print(f"\nmatrix[0][0] = {matrix[0][0]}")  # 1
    print(f"matrix[2][1] = {matrix[2][1]}")  # 8

    # Правильное создание матрицы через comprehension
    size = 3
    good_matrix = [[0 for _ in range(size)] for _ in range(size)]
    print(f"\nПравильная матрица: {good_matrix}")
    good_matrix[0][0] = 99
    print(f"После good_matrix[0][0] = 99: {good_matrix} (меняется только одна ячейка)")

    # Транспонирование матрицы (строки ↔ столбцы)
    transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print(f"\nТранспонированная:")
    for row in transposed:
        print(f"  {row}")

    # Сумма элементов на диагонали
    diagonal_sum = sum(matrix[i][i] for i in range(len(matrix)))
    print(f"\nСумма главной диагонали: {diagonal_sum}")  # 1+5+9 = 15


def demo_advanced():
    """Продвинутые операции со списками."""
    print("\n" + "=" * 50)
    print("📌 ПРОДВИНУТЫЕ ОПЕРАЦИИ")
    print("=" * 50)

    # any() / all() со списками
    nums = [2, 4, 6, 8]
    print(f"all(n % 2 == 0 for n in nums) = {all(n % 2 == 0 for n in nums)}")  # все чётные
    print(f"any(n > 5 for n in nums) = {any(n > 5 for n in nums)}")  # есть > 5

    # filter/map (функциональный стиль)
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"filter (чётные): {evens}")
    print(f"map (×2): {doubled}")

    # Распаковка (unpacking)
    first, *middle, last = [1, 2, 3, 4, 5]
    print(f"\nРаспаковка: first={first}, middle={middle}, last={last}")

    # Объединение списков
    a, b = [1, 2], [3, 4]
    combined = a + b
    print(f"Конкатенация: {a} + {b} = {combined}")

    # Удаление дубликатов через set
    duplicates = [1, 2, 2, 3, 3, 3, 4]
    unique = list(set(duplicates))
    print(f"Удаление дубликатов: {duplicates} → {unique}")

    # Сохранение порядка при удалении дубликатов (Python 3.7+)
    unique_ordered = list(dict.fromkeys(duplicates))
    print(f"С сохранением порядка: {unique_ordered}")

    # Сравнение списков
    print(f"\n[1, 2, 3] == [1, 2, 3]: {[1, 2, 3] == [1, 2, 3]}")
    print(f"[1, 2, 3] < [1, 2, 4]: {[1, 2, 3] < [1, 2, 4]}")  # лексикографическое


def main():
    """Главная функция."""
    print("🐍 УРОК 07: СПИСКИ (list)")
    print("=" * 50)

    demo_creation()
    demo_indexing_slicing()
    demo_methods()
    demo_copy()
    demo_stack_queue()
    demo_multidimensional()
    demo_advanced()

    print("\n" + "=" * 50)
    print("✅ Урок 07 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. Список — изменяемая упорядоченная коллекция")
    print("  2. Срезы работают так же как у строк, но списки можно изменять через срезы")
    print("  3. Shallow copy копирует только верхний уровень (вложенные объекты — ссылки)")
    print("  4. Для стека: append/pop, для очереди: collections.deque")
    print("  5. Осторожно: [[0]*3]*3 создаёт ссылки на один вложенный список!")
    print("=" * 50)


if __name__ == "__main__":
    main()
