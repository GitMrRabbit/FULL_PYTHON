"""
УРОК 09: Словари (dict)
========================

Демонстрирует:
- Создание словарей разными способами
- Доступ к элементам: [] vs .get()
- Основные методы: keys(), values(), items(), update(), pop(), popitem(), setdefault()
- defaultdict, Counter, OrderedDict из collections
- Dict comprehensions
- Вложенные словари
"""


def demo_basics():
    """Создание и базовые операции со словарями."""
    print("=" * 50)
    print("📌 СЛОВАРИ — ОСНОВЫ")
    print("=" * 50)

    # Создание словарей
    d1 = {"name": "Анна", "age": 25, "city": "Москва"}
    d2 = dict(name="Борис", age=30, city="Питер")  # только строковые ключи!
    d3 = dict([("key1", 1), ("key2", 2)])  # из списка пар
    d4 = dict(zip(["a", "b", "c"], [1, 2, 3]))  # из двух списков
    d5 = {}  # пустой
    d6 = dict.fromkeys(["x", "y", "z"], 0)  # все ключи с одним значением

    print(f"d1 = {d1}")
    print(f"d2 = {d2}")
    print(f"d3 = {d3}")
    print(f"d4 = {d4}")
    print(f"d6 = {d6}")

    # Доступ к элементам
    print(f"\nДоступ:")
    print(f"  d1['name'] = {d1['name']}")
    # print(d1['country'])  # KeyError!

    # .get() — безопасный доступ (без ошибки)
    print(f"  d1.get('name') = {d1.get('name')}")
    print(f"  d1.get('country') = {d1.get('country')}")  # None
    print(f"  d1.get('country', 'Россия') = {d1.get('country', 'Россия')}")  # значение по умолчанию

    # Добавление/изменение
    d1["email"] = "anna@example.com"  # новый ключ
    d1["age"] = 26  # изменение существующего
    print(f"\nПосле добавления/изменения: {d1}")

    # Удаление
    removed = d1.pop("city")
    print(f"pop('city') → '{removed}', d1 = {d1}")
    popped = d1.popitem()  # удаляет и возвращает ПОСЛЕДНЮЮ пару (Python 3.7+)
    print(f"popitem() → {popped}, d1 = {d1}")
    del d1["age"]  # удаление через del
    print(f"del d1['age'] → {d1}")

    # Проверка наличия ключа
    print(f"\n'name' in d1: {'name' in d1}")
    print(f"'age' in d1: {'age' in d1}")


def demo_methods():
    """Основные методы словарей."""
    print("\n" + "=" * 50)
    print("📌 МЕТОДЫ СЛОВАРЕЙ")
    print("=" * 50)

    user = {"name": "Анна", "age": 25, "city": "Москва"}

    # keys(), values(), items()
    print(f"Ключи: {list(user.keys())}")
    print(f"Значения: {list(user.values())}")
    print(f"Пары: {list(user.items())}")

    # Итерация
    print("\nИтерация:")
    for key in user:
        print(f"  {key}: {user[key]}")

    print("\nЧерез .items():")
    for key, value in user.items():
        print(f"  {key}: {value}")

    # update() — объединение словарей
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 20, "c": 30}  # 'b' перезапишется!
    d1.update(d2)
    print(f"\nupdate: d1 = {d1}")

    # | оператор (Python 3.9+)
    a = {"x": 1, "y": 2}
    b = {"y": 20, "z": 30}
    merged = a | b  # новый словарь
    print(f"a | b = {merged}")
    a |= b  # на месте
    print(f"a |= b → {a}")

    # setdefault() — получить значение, а если нет ключа — создать с значением по умолчанию
    counter_dict = {}
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    for word in words:
        counter_dict.setdefault(word, 0)
        counter_dict[word] += 1
    print(f"\nПодсчёт через setdefault: {counter_dict}")


def demo_collections():
    """defaultdict, Counter, OrderedDict."""
    print("\n" + "=" * 50)
    print("📌 defaultdict, Counter, OrderedDict")
    print("=" * 50)

    from collections import defaultdict, Counter, OrderedDict

    # defaultdict — словарь с автоматическим значением по умолчанию
    print("--- defaultdict ---")
    dd = defaultdict(int)  # значение по умолчанию — int() = 0
    words = ["a", "b", "a", "c", "b", "a"]
    for w in words:
        dd[w] += 1  # не нужно проверять наличие ключа!
    print(f"Подсчёт через defaultdict: {dict(dd)}")

    dd_list = defaultdict(list)
    pairs = [("fruit", "apple"), ("fruit", "banana"), ("veg", "carrot")]
    for category, item in pairs:
        dd_list[category].append(item)
    print(f"Группировка: {dict(dd_list)}")

    # Counter — специализированный словарь для подсчёта
    print("\n--- Counter ---")
    text = "abracadabra"
    counter = Counter(text)
    print(f"Counter('{text}') = {counter}")
    print(f"  Топ-3: {counter.most_common(3)}")
    print(f"  Всего букв: {sum(counter.values())}")

    # Арифметика с Counter
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2)
    print(f"\n  c1 + c2 = {c1 + c2}")  # сложение
    print(f"  c1 - c2 = {c1 - c2}")  # вычитание (только положительные)
    print(f"  c1 & c2 = {c1 & c2}")  # пересечение (минимумы)
    print(f"  c1 | c2 = {c1 | c2}")  # объединение (максимумы)

    # OrderedDict — словарь, помнящий порядок вставки
    # В Python 3.7+ обычный dict тоже помнит порядок!
    # Но OrderedDict имеет дополнительные методы:
    print("\n--- OrderedDict ---")
    od = OrderedDict()
    od["first"] = 1
    od["second"] = 2
    od["third"] = 3
    print(f"OrderedDict: {od}")
    od.move_to_end("first")  # переместить в конец
    print(f"move_to_end('first'): {od}")
    print(f"popitem(last=False): {od.popitem(last=False)}")  # удалить ПЕРВЫЙ


def demo_comprehensions():
    """Dict comprehensions."""
    print("\n" + "=" * 50)
    print("📌 DICT COMPREHENSIONS")
    print("=" * 50)

    # Базовый синтаксис: {key_expr: value_expr for item in iterable}

    squares = {x: x ** 2 for x in range(5)}
    print(f"Квадраты: {squares}")

    # С условием
    evens = {x: x ** 2 for x in range(10) if x % 2 == 0}
    print(f"Квадраты чётных: {evens}")

    # Из двух списков
    keys = ["name", "age", "city"]
    values = ["Анна", 25, "Москва"]
    combined = {k: v for k, v in zip(keys, values)}
    print(f"Из zip: {combined}")

    # Переворот словаря (ключ ↔ значение)
    original = {"a": 1, "b": 2, "c": 3}
    flipped = {v: k for k, v in original.items()}
    print(f"Переворот: {original} → {flipped}")

    # Фильтрация по значению
    scores = {"Анна": 85, "Борис": 92, "Виктор": 78, "Галина": 95}
    high_scores = {name: score for name, score in scores.items() if score >= 90}
    print(f"Высокие баллы (≥90): {high_scores}")


def demo_nested():
    """Вложенные словари."""
    print("\n" + "=" * 50)
    print("📌 ВЛОЖЕННЫЕ СЛОВАРИ")
    print("=" * 50)

    # База данных пользователей
    users = {
        "user1": {
            "name": "Анна",
            "age": 25,
            "contacts": {"email": "anna@mail.ru", "phone": "+79001234567"}
        },
        "user2": {
            "name": "Борис",
            "age": 30,
            "contacts": {"email": "boris@mail.ru", "phone": "+79007654321"}
        }
    }

    print("Доступ к вложенным данным:")
    print(f"  users['user1']['name'] = {users['user1']['name']}")
    print(f"  users['user2']['contacts']['email'] = {users['user2']['contacts']['email']}")

    # Безопасный доступ через цепочку .get()
    phone = users.get("user3", {}).get("contacts", {}).get("phone", "Нет данных")
    print(f"\nБезопасный доступ: users['user3']['contacts']['phone'] = {phone}")

    # Итерация по вложенному словарю
    print("\nВсе пользователи:")
    for uid, data in users.items():
        print(f"  {uid}: {data['name']}, {data['age']} лет, {data['contacts']['email']}")


def demo_practical():
    """Практические приёмы."""
    print("\n" + "=" * 50)
    print("📌 ПРАКТИЧЕСКИЕ ПРИЁМЫ")
    print("=" * 50)

    # Группировка по признаку
    students = [
        {"name": "Анна", "grade": "A"},
        {"name": "Борис", "grade": "B"},
        {"name": "Виктор", "grade": "A"},
        {"name": "Галина", "grade": "C"},
    ]

    grouped = {}
    for s in students:
        grouped.setdefault(s["grade"], []).append(s["name"])
    print(f"Группировка по оценкам: {grouped}")

    # Частотный анализ текста
    text = "python is great python is fun python is powerful"
    words = text.lower().split()
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1  # идиоматичный способ
    print(f"\nЧастоты слов: {freq}")

    # Сортировка словаря
    data = {"banana": 3, "apple": 4, "cherry": 1}
    sorted_by_key = dict(sorted(data.items()))
    sorted_by_value = dict(sorted(data.items(), key=lambda x: x[1]))
    print(f"\nСортировка по ключу: {sorted_by_key}")
    print(f"Сортировка по значению: {sorted_by_value}")


def main():
    """Главная функция."""
    print("🐍 УРОК 09: СЛОВАРИ (dict)")
    print("=" * 50)

    demo_basics()
    demo_methods()
    demo_collections()
    demo_comprehensions()
    demo_nested()
    demo_practical()

    print("\n" + "=" * 50)
    print("✅ Урок 09 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. Словарь — коллекция ключ:значение, O(1) доступ по ключу")
    print("  2. .get() — безопасный доступ с значением по умолчанию")
    print("  3. defaultdict и Counter — мощные расширения из collections")
    print("  4. Dict comprehensions — компактное создание словарей")
    print("  5. Python 3.7+: словари сохраняют порядок вставки")
    print("=" * 50)


if __name__ == "__main__":
    main()
