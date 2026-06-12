"""
Урок 20: Итераторы и Генераторы
================================

Темы:
  - Итераторы: __iter__(), __next__(), StopIteration
  - Генераторы: yield, yield from
  - Генераторные выражения: (... for x in ...)
  - send(), throw(), close() — продвинутое управление
  - itertools — мощные итераторы
  - Практические примеры: пайплайны обработки данных
"""

import itertools
from typing import Iterator, Generator


# =============================================================================
# 1. ИТЕРАТОРЫ (повторение и углубление)
# =============================================================================

class Fibonacci:
    """
    Итератор чисел Фибоначчи.
    Бесконечный? Нет — до max_n.
    """

    def __init__(self, max_n: int):
        self.max_n = max_n
        self.n = 0
        self.a, self.b = 0, 1

    def __iter__(self) -> "Fibonacci":
        return self

    def __next__(self) -> int:
        if self.n >= self.max_n:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.n += 1
        return value

    def __len__(self) -> int:
        return self.max_n


def iterators_demo():
    """Демонстрация итераторов."""
    print("=" * 60)
    print("1. ИТЕРАТОРЫ")
    print("=" * 60)

    fib = Fibonacci(10)
    print(f"Первые {len(fib)} чисел Фибоначчи:")
    for n in fib:
        print(f"  {n}", end="")
    print()

    # Ручное использование
    fib2 = Fibonacci(5)
    it = iter(fib2)
    print(f"next(it): {next(it)}, {next(it)}, {next(it)}")
    print(f"list(it): {list(it)}")  # Оставшиеся 2 элемента


# =============================================================================
# 2. ГЕНЕРАТОРЫ (yield)
# =============================================================================

def count_up_to(n: int) -> Generator[int, None, None]:
    """
    Генератор: функция с yield.
    Вместо return использует yield — "замораживает" состояние.
    """
    i = 1
    while i <= n:
        yield i
        i += 1


def infinite_counter(start: int = 0) -> Generator[int, None, None]:
    """Бесконечный генератор-счётчик."""
    while True:
        yield start
        start += 1


def read_lines_batched(filename: str, batch_size: int = 3) -> Generator[list[str], None, None]:
    """
    Практический пример: чтение большого файла батчами.
    Не загружает весь файл в память!
    """
    batch = []
    for line in open(filename, "r", encoding="utf-8"):
        batch.append(line.rstrip())
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:  # Остаток
        yield batch


def generators_demo():
    """Демонстрация генераторов."""
    print("\n" + "=" * 60)
    print("2. ГЕНЕРАТОРЫ (yield)")
    print("=" * 60)

    # Простой генератор
    gen = count_up_to(5)
    print(f"count_up_to(5): {list(gen)}")

    # Бесконечный генератор
    counter = infinite_counter(100)
    print("infinite_counter (первые 5):", end=" ")
    for _, n in zip(range(5), counter):
        print(n, end=" ")
    print()

    # Генератор не хранит всё в памяти!
    big_range = count_up_to(1_000_000)
    print(f"Размер big_range в памяти: {big_range.__sizeof__()} байт")
    # Сравните с list(range(1_000_000)) — ~8 МБ!


# =============================================================================
# 3. ГЕНЕРАТОРНЫЕ ВЫРАЖЕНИЯ
# =============================================================================

def generator_expressions_demo():
    """Демонстрация генераторных выражений."""
    print("\n" + "=" * 60)
    print("3. ГЕНЕРАТОРНЫЕ ВЫРАЖЕНИЯ")
    print("=" * 60)

    # List comprehension → весь список в памяти
    squares_list = [x ** 2 for x in range(10)]
    print(f"List comprehension: {squares_list}")

    # Generator expression → ленивое вычисление
    squares_gen = (x ** 2 for x in range(10))
    print(f"Generator expression: {squares_gen}")  # Не вычисляется сразу!

    print("Итерация по генератору:", end=" ")
    for sq in squares_gen:
        print(sq, end=" ")
    print()

    # Генератор можно передать в sum(), max(), min() без создания списка
    total = sum(x ** 2 for x in range(1_000_000))
    print(f"sum(x**2 for x in range(1M)): {total}")

    # Вложенные генераторные выражения
    pairs = ((x, y) for x in range(3) for y in range(2))
    print(f"Декартово произведение: {list(pairs)}")


# =============================================================================
# 4. yield from — ДЕЛЕГИРОВАНИЕ
# =============================================================================

def chain_generators(*iterables) -> Generator:
    """
    Аналог itertools.chain, но на yield from.
    yield from делегирует итерацию другому итератору.
    """
    for it in iterables:
        yield from it  # Вместо: for item in it: yield item


def flatten(nested_list) -> Generator:
    """
    Рекурсивное разворачивание вложенных списков через yield from.
    """
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)  # Рекурсивно!
        else:
            yield item


def yield_from_demo():
    """Демонстрация yield from."""
    print("\n" + "=" * 60)
    print("4. yield from")
    print("=" * 60)

    # Цепочка итераторов
    result = list(chain_generators([1, 2], "ab", (True, False)))
    print(f"chain_generators: {result}")

    # Разворачивание
    nested = [1, [2, [3, 4], 5], 6, [7, 8]]
    flat = list(flatten(nested))
    print(f"flatten({nested}): {flat}")


# =============================================================================
# 5. send(), throw(), close() — ПРОДВИНУТОЕ УПРАВЛЕНИЕ
# =============================================================================

def accumulator() -> Generator[float, float, float]:
    """
    Генератор-аккумулятор.
    - yield отдаёт текущую сумму
    - send(x) добавляет x к сумме
    - throw/close управляют завершением
    """
    total = 0.0
    count = 0
    while True:
        try:
            value = yield total  # Отдаём total, принимаем значение
            if value is None:
                continue
            total += value
            count += 1
        except ValueError as e:
            print(f"  [Ошибка: {e}]")
            # Продолжаем работу!
            yield total
        except GeneratorExit:
            print(f"\n  [Закрытие. Итого: {total:.2f}, операций: {count}]")
            return total


def advanced_generator_demo():
    """Демонстрация send(), throw(), close()."""
    print("\n" + "=" * 60)
    print("5. ПРОДВИНУТОЕ УПРАВЛЕНИЕ ГЕНЕРАТОРОМ")
    print("=" * 60)

    acc = accumulator()

    # Первый вызов — только next() или send(None)
    total = next(acc)
    print(f"Начало: {total}")

    # send() — передаём значение в генератор
    total = acc.send(10)
    print(f"send(10) → {total}")
    total = acc.send(20)
    print(f"send(20) → {total}")
    total = acc.send(5.5)
    print(f"send(5.5) → {total}")

    # throw() — бросить исключение ВНУТРИ генератора
    total = acc.throw(ValueError, "Тестовая ошибка")
    print(f"throw(ValueError) → {total}")

    # close() — закрыть генератор
    acc.close()
    print("Генератор закрыт")


# =============================================================================
# 6. ITERTOOLS — ПРОДВИНУТЫЕ ИТЕРАТОРЫ
# =============================================================================

def itertools_demo():
    """Демонстрация itertools."""
    print("\n" + "=" * 60)
    print("6. ITERTOOLS")
    print("=" * 60)

    # Бесконечные итераторы
    print("count(10, 2):", list(itertools.islice(itertools.count(10, 2), 5)))
    print("cycle('AB'):", list(itertools.islice(itertools.cycle("AB"), 6)))
    print("repeat('X', 3):", list(itertools.repeat("X", 3)))

    # Комбинаторика
    print(f"\ncombinations('ABCD', 2): {list(itertools.combinations('ABCD', 2))}")
    print(f"permutations('AB', 2):   {list(itertools.permutations('AB', 2))}")
    print(f"product('AB', '12'):     {list(itertools.product('AB', '12'))}")

    # Соединение и группировка
    print(f"\nchain([1,2], 'ab'):    {list(itertools.chain([1, 2], 'ab'))}")

    # Группировка по ключу
    data = [("a", 1), ("a", 2), ("b", 3), ("b", 4)]
    grouped = itertools.groupby(data, key=lambda x: x[0])
    print("groupby:")
    for key, group in grouped:
        print(f"  {key}: {list(group)}")

    # Фильтрация
    print(f"\ncompress('ABCD', [1,0,1,0]): {list(itertools.compress('ABCD', [1, 0, 1, 0]))}")
    print(f"dropwhile(lambda x: x<3, [1,2,3,1,2]): "
          f"{list(itertools.dropwhile(lambda x: x < 3, [1, 2, 3, 1, 2]))}")
    print(f"takewhile(lambda x: x<3, [1,2,3,1,2]): "
          f"{list(itertools.takewhile(lambda x: x < 3, [1, 2, 3, 1, 2]))}")

    # Агрегация
    print(f"\naccumulate([1,2,3,4]): {list(itertools.accumulate([1, 2, 3, 4]))}")

    # pairwise (Python 3.10+)
    if hasattr(itertools, "pairwise"):
        print(f"pairwise('ABCD'): {list(itertools.pairwise('ABCD'))}")


# =============================================================================
# 7. ПРАКТИЧЕСКИЙ ПРИМЕР: ПАЙПЛАЙН ОБРАБОТКИ ДАННЫХ
# =============================================================================

def read_logs() -> Generator[str, None, None]:
    """Генератор строк лога (имитация больших данных)."""
    for i in range(20):
        yield f"192.168.1.{i % 5} - - [{2024}-{i % 12 + 1:02d}-01] "
        f"\"GET /page{i} HTTP/1.1\" {200 if i % 3 else 404} {i * 10}"


def parse_logs(lines: Generator[str, None, None]) -> Generator[dict, None, None]:
    """Парсинг строк лога в словари."""
    import re
    pattern = r"(\S+) .*\[(\d{4}-\d{2}-\d{2})\].*\" (\d+) .* (\d+)$"
    for line in lines:
        match = re.search(pattern, line)
        if match:
            yield {
                "ip": match.group(1),
                "date": match.group(2),
                "status": match.group(3),
                "size": match.group(4),
            }


def filter_errors(records: Generator[dict, None, None], status: str) -> Generator[dict, None, None]:
    """Фильтрация: только записи с определённым статусом."""
    for rec in records:
        if rec["status"] == status:
            yield rec


def pipeline_demo():
    """
    Практический пример: пайплайн обработки данных на генераторах.
    read_logs → parse_logs → filter_errors → агрегация.

    Преимущества:
      - Каждый шаг — отдельный генератор
      - Данные не хранятся в памяти (lazy evaluation)
      - Легко добавить/убрать шаг пайплайна
    """
    print("\n" + "=" * 60)
    print("7. ПРАКТИЧЕСКИЙ ПРИМЕР: ПАЙПЛАЙН")
    print("=" * 60)

    # Строим пайплайн
    lines = read_logs()
    records = parse_logs(lines)
    errors = filter_errors(records, status="404")

    print("Записи с ошибкой 404:")
    for rec in errors:
        print(f"  {rec['ip']} | {rec['date']} | {rec['status']} | {rec['size']} байт")


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    iterators_demo()
    generators_demo()
    generator_expressions_demo()
    yield_from_demo()
    advanced_generator_demo()
    itertools_demo()
    pipeline_demo()

    print("\n" + "=" * 60)
    print("✅ УРОК 20 ЗАВЕРШЁН: ГЕНЕРАТОРЫ И ИТЕРАТОРЫ ОСВОЕНЫ!")
    print("=" * 60)
