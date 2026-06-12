"""
УРОК 08: Кортежи (tuple) и Множества (set)
============================================

Демонстрирует:
- Кортежи: неизменяемые последовательности, распаковка, именованные кортежи
- Множества: уникальные элементы, операции над множествами
- frozenset: неизменяемое множество
"""


# ============================================================
# ЧАСТЬ 1: КОРТЕЖИ (tuple)
# ============================================================

def demo_tuple_basics():
    """Основы кортежей."""
    print("=" * 50)
    print("📌 КОРТЕЖИ (tuple) — ОСНОВЫ")
    print("=" * 50)

    # Создание кортежей
    t1 = (1, 2, 3)
    t2 = 1, 2, 3        # скобки не обязательны!
    t3 = (42,)           # кортеж из одного элемента (запятая ВАЖНА!)
    t4 = ()              # пустой кортеж
    t5 = tuple([1, 2, 3])  # из списка
    t6 = tuple("abc")    # из строки

    print(f"t1 = (1, 2, 3)  → {t1}")
    print(f"t2 = 1, 2, 3    → {t2}")
    print(f"t3 = (42,)       → {t3}  (запятая обязательна для одного элемента!)")
    print(f"t4 = ()          → {t4}")
    print(f"tuple('abc')     → {t6}")

    # Без запятой это НЕ кортеж!
    not_tuple = (42)
    print(f"\n⚠️ (42) без запятой — это int: {type(not_tuple).__name__}")

    # Доступ по индексу (как у списков)
    t = (10, 20, 30, 40, 50)
    print(f"\nt = {t}")
    print(f"t[0] = {t[0]}")
    print(f"t[-1] = {t[-1]}")
    print(f"t[1:4] = {t[1:4]}")

    # НЕИЗМЕНЯЕМОСТЬ
    try:
        t[0] = 999
    except TypeError as e:
        print(f"\n❌ t[0] = 999 → TypeError: кортежи неизменяемы!")

    # Но! Если кортеж содержит изменяемый объект — его можно изменить
    tricky = (1, [2, 3], 4)
    print(f"\nХитрый кортеж: {tricky}")
    tricky[1][0] = 999
    print(f"После tricky[1][0] = 999: {tricky}  ← список внутри изменился!")


def demo_tuple_unpacking():
    """Распаковка кортежей."""
    print("\n" + "=" * 50)
    print("📌 РАСПАКОВКА КОРТЕЖЕЙ")
    print("=" * 50)

    # Базовая распаковка
    coordinates = (10, 20)
    x, y = coordinates
    print(f"coordinates = {coordinates} → x={x}, y={y}")

    # Распаковка с *
    values = (1, 2, 3, 4, 5)
    first, *middle, last = values
    print(f"{values} → first={first}, middle={middle}, last={last}")

    # Обмен значений (swap) — на самом деле распаковка!
    a, b = 10, 20
    a, b = b, a
    print(f"Swap: a={a}, b={b}")

    # Распаковка в функции (возврат нескольких значений)
    def min_max(items):
        return min(items), max(items)  # возвращает кортеж!

    result = min_max([3, 1, 4, 1, 5, 9])
    print(f"min_max → {result} (тип: {type(result).__name__})")
    mn, mx = min_max([3, 1, 4, 1, 5, 9])
    print(f"Распаковка: min={mn}, max={mx}")

    # _ для игнорирования значений
    _, important, _ = (1, 42, 3)
    print(f"Пропуск через _: important={important}")


def demo_namedtuple():
    """Именованные кортежи (namedtuple)."""
    print("\n" + "=" * 50)
    print("📌 ИМЕНОВАННЫЕ КОРТЕЖИ (namedtuple)")
    print("=" * 50)

    from collections import namedtuple

    # Создание типа
    Point = namedtuple("Point", ["x", "y"])
    Color = namedtuple("Color", "red green blue")

    # Создание экземпляров
    p = Point(10, 20)
    c = Color(255, 128, 0)

    # Доступ по имени (как у объекта) и по индексу (как у кортежа)
    print(f"p = {p}")
    print(f"p.x = {p.x}, p.y = {p.y}")
    print(f"p[0] = {p[0]}, p[1] = {p[1]}")

    # Распаковка работает
    x, y = p
    print(f"Распаковка: x={x}, y={y}")

    # НЕИЗМЕНЯЕМЫ (как и обычные кортежи)
    try:
        p.x = 999
    except AttributeError as e:
        print(f"❌ p.x = 999 → AttributeError (нельзя изменить)")

    # _asdict() — преобразование в словарь
    print(f"p._asdict() = {p._asdict()}")

    # _replace() — создаёт новый кортеж с изменённым полем
    p2 = p._replace(x=99)
    print(f"p._replace(x=99) → {p2}")

    # Практический пример: запись в CSV/БД
    Person = namedtuple("Person", "name age city")
    people = [
        Person("Анна", 25, "Москва"),
        Person("Борис", 30, "Питер"),
    ]
    for person in people:
        print(f"  {person.name}, {person.age} лет, {person.city}")


# ============================================================
# ЧАСТЬ 2: МНОЖЕСТВА (set)
# ============================================================

def demo_set_basics():
    """Основы множеств."""
    print("\n" + "=" * 50)
    print("📌 МНОЖЕСТВА (set) — ОСНОВЫ")
    print("=" * 50)

    # Создание множеств
    s1 = {1, 2, 3, 4, 5}
    s2 = set([1, 2, 2, 3, 3, 3])  # из списка (дубликаты удалятся)
    s3 = set("hello")  # из строки
    empty = set()       # ПУСТОЕ множество ({} — это словарь!)

    print(f"s1 = {s1}")
    print(f"set([1,2,2,3,3,3]) = {s2}  (дубликаты удалены!)")
    print(f"set('hello') = {s3}")
    print(f"⚠️ empty = set(), НЕ {{}} ({{}} это dict, тип: {type({}).__name__})")

    # Основные свойства
    # 1. Уникальность — дубликаты автоматически удаляются
    # 2. Неупорядоченность — порядок не гарантирован (но в CPython 3.7+ — порядок вставки)
    # 3. Элементы должны быть ХЭШИРУЕМЫМИ (нельзя список внутрь множества)

    try:
        bad = {[1, 2], [3, 4]}
    except TypeError as e:
        print(f"\n❌ {{[1,2], [3,4]}} → TypeError: список не хэшируется")

    # Основные операции
    s = {1, 2, 3}
    s.add(4)
    print(f"\nadd(4): {s}")
    s.add(2)  # повторное добавление игнорируется
    print(f"add(2) повторно: {s} (ничего не изменилось)")

    s.remove(3)  # удалить элемент (KeyError если нет)
    print(f"remove(3): {s}")

    s.discard(99)  # удалить, НЕ вызывая ошибку если нет
    print(f"discard(99): {s} (нет ошибки)")

    popped = s.pop()  # удалить и вернуть случайный элемент
    print(f"pop() → {popped}, осталось: {s}")

    # Проверка вхождения (O(1) в среднем!)
    print(f"\n2 in {s}: {2 in s}")
    print(f"99 in {s}: {99 in s}")


def demo_set_operations():
    """Операции над множествами."""
    print("\n" + "=" * 50)
    print("📌 ОПЕРАЦИИ НАД МНОЖЕСТВАМИ")
    print("=" * 50)

    A = {1, 2, 3, 4, 5}
    B = {4, 5, 6, 7, 8}

    print(f"A = {A}")
    print(f"B = {B}")

    # Объединение (union) — элементы из A ИЛИ B
    print(f"\nA | B  = {A | B}   (объединение)")
    print(f"A.union(B) = {A.union(B)}")

    # Пересечение (intersection) — элементы из A И B
    print(f"\nA & B  = {A & B}   (пересечение)")
    print(f"A.intersection(B) = {A.intersection(B)}")

    # Разность (difference) — элементы из A, которых нет в B
    print(f"\nA - B  = {A - B}   (разность)")
    print(f"A.difference(B) = {A.difference(B)}")

    # Симметрическая разность — элементы в A ИЛИ B, но не в обоих
    print(f"\nA ^ B  = {A ^ B}   (симметрическая разность)")
    print(f"A.symmetric_difference(B) = {A.symmetric_difference(B)}")

    # Проверка подмножества/надмножества
    small = {1, 2}
    big = {1, 2, 3, 4}
    print(f"\n{small}.issubset({big}) = {small.issubset(big)}")
    print(f"{small} <= {big} = {small <= big}")  # подмножество
    print(f"{big}.issuperset({small}) = {big.issuperset(small)}")
    print(f"{big} >= {small} = {big >= small}")  # надмножество
    print(f"{big} > {small} = {big > small}")    # строгое надмножество

    # Непересекающиеся множества (disjoint)
    X = {1, 2, 3}
    Y = {4, 5, 6}
    print(f"\n{bool(X & Y)} — X и Y пересекаются? {bool(X & Y)}")
    print(f"X.isdisjoint(Y) = {X.isdisjoint(Y)}")

    # Обновление на месте (in-place)
    s = {1, 2, 3}
    s.update({3, 4, 5})  # s |= other
    print(f"\nupdate: {s}")
    s.intersection_update({2, 3, 6})  # s &= other
    print(f"intersection_update: {s}")


def demo_frozenset():
    """Неизменяемое множество (frozenset)."""
    print("\n" + "=" * 50)
    print("📌 FROZENSET (неизменяемое множество)")
    print("=" * 50)

    # frozenset — неизменяемая версия set
    # Можно использовать как ключ словаря или элемент множества!

    fs = frozenset([1, 2, 3])
    print(f"frozenset: {fs}")
    print(f"Тип: {type(fs).__name__}")

    # Нельзя изменить
    try:
        fs.add(4)
    except AttributeError as e:
        print(f"❌ fs.add(4) → AttributeError")

    # Но можно использовать в словаре!
    cache = {
        frozenset(["apple", "banana"]): "фруктовый микс",
        frozenset(["carrot", "potato"]): "овощной микс",
    }
    print(f"\nСловарь с frozenset-ключами:")
    for key, val in cache.items():
        print(f"  {set(key)} → {val}")

    # Операции над frozenset (без изменения!)
    a = frozenset([1, 2, 3])
    b = frozenset([3, 4, 5])
    print(f"\na | b = {a | b}")  # объединение
    print(f"a & b = {a & b}")  # пересечение


def demo_practical():
    """Практическое применение множеств."""
    print("\n" + "=" * 50)
    print("📌 ПРАКТИЧЕСКОЕ ПРИМЕНЕНИЕ")
    print("=" * 50)

    # Удаление дубликатов из списка
    items = [1, 2, 2, 3, 3, 3, 4, 5, 5]
    unique = list(set(items))
    print(f"Удаление дубликатов: {items} → {unique}")

    # Поиск общих элементов
    user1_tags = {"python", "django", "docker"}
    user2_tags = {"python", "javascript", "docker", "react"}
    common = user1_tags & user2_tags
    print(f"Общие интересы: {common}")

    # Проверка уникальности
    def all_unique(items):
        return len(items) == len(set(items))

    print(f"all_unique([1,2,3]): {all_unique([1, 2, 3])}")
    print(f"all_unique([1,2,2]): {all_unique([1, 2, 2])}")

    # Подсчёт уникальных слов в тексте
    text = "python is great and python is fun"
    words = text.lower().split()
    unique_words = set(words)
    print(f"Уникальных слов: {len(unique_words)} из {len(words)} всего")
    print(f"  Слова: {unique_words}")


def main():
    """Главная функция."""
    print("🐍 УРОК 08: КОРТЕЖИ И МНОЖЕСТВА")
    print("=" * 50)

    # Кортежи
    demo_tuple_basics()
    demo_tuple_unpacking()
    demo_namedtuple()

    # Множества
    demo_set_basics()
    demo_set_operations()
    demo_frozenset()
    demo_practical()

    print("\n" + "=" * 50)
    print("✅ Урок 08 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. Кортеж — неизменяемый список, быстрее и занимает меньше памяти")
    print("  2. namedtuple — кортеж с доступом по имени поля")
    print("  3. Множество — коллекция уникальных элементов, O(1) поиск")
    print("  4. frozenset — неизменяемое множество, можно ключом словаря")
    print("  5. Операции над множествами: | (union), & (intersection), - (diff), ^ (sym_diff)")
    print("=" * 50)


if __name__ == "__main__":
    main()
