"""
УРОК 05: Условные операторы (if / elif / else / match-case)
=============================================================

Демонстрирует:
- if, elif, else — классические условные конструкции
- Тернарный оператор (однострочный if/else)
- match/case (Python 3.10+) — структурное сопоставление с образцом
- Вложенные условия
- Проверку нескольких условий
- Truthy/Falsy значения в условиях
"""


def demo_if_else():
    """Базовые условные конструкции."""
    print("=" * 50)
    print("📌 IF / ELIF / ELSE")
    print("=" * 50)

    age = 18

    # Простой if
    if age >= 18:
        print("Вы совершеннолетний.")
    else:
        print("Вы несовершеннолетний.")

    # if / elif / else — множественный выбор
    score = 85

    if score >= 90:
        grade = "A (Отлично)"
    elif score >= 80:
        grade = "B (Хорошо)"
    elif score >= 70:
        grade = "C (Удовлетворительно)"
    elif score >= 60:
        grade = "D (Плохо)"
    else:
        grade = "F (Неудовлетворительно)"

    print(f"Оценка за {score} баллов: {grade}")

    # Вложенные условия
    temperature = 25
    is_raining = True

    if temperature > 20:
        print("На улице тепло.")
        if is_raining:
            print("  Но идёт дождь — возьмите зонт!")
        else:
            print("  Отличная погода для прогулки!")
    else:
        print("На улице прохладно.")
        if temperature < 0:
            print("  Наденьте шапку и перчатки!")
        else:
            print("  Достаточно лёгкой куртки.")


def demo_ternary():
    """Тернарный оператор (однострочный if/else)."""
    print("\n" + "=" * 50)
    print("📌 ТЕРНАРНЫЙ ОПЕРАТОР")
    print("=" * 50)

    # Синтаксис: value_if_true if condition else value_if_false
    age = 17
    status = "совершеннолетний" if age >= 18 else "несовершеннолетний"
    print(f"Возраст {age}: {status}")

    # Пример с вычислением
    x = -5
    absolute = x if x >= 0 else -x
    print(f"|{x}| = {absolute}")

    # Можно использовать с функциями
    def is_even(n):
        return "чётное" if n % 2 == 0 else "нечётное"

    for num in [1, 2, 3, 4, 5]:
        print(f"  {num} — {is_even(num)}")

    # Кортежный трюк (менее читаемый, но работает)
    # (value_if_false, value_if_true)[condition]
    n = 7
    parity = ("нечётное", "чётное")[n % 2 == 0]
    print(f"  {n} — {parity} (кортежный трюк)")


def demo_match_case():
    """match/case — структурное сопоставление с образцом (Python 3.10+)."""
    print("\n" + "=" * 50)
    print("📌 MATCH / CASE (Python 3.10+)")
    print("=" * 50)

    # match/case — это НЕ switch/case из других языков!
    # Это мощный механизм сопоставления с образцом (pattern matching)

    # Простой пример — аналог switch
    def http_status_description(code):
        match code:
            case 200:
                return "OK"
            case 201:
                return "Created"
            case 400:
                return "Bad Request"
            case 404:
                return "Not Found"
            case 500:
                return "Internal Server Error"
            case _:  # _ — wildcard (значение по умолчанию)
                return f"Unknown status: {code}"

    for status in [200, 404, 500, 999]:
        print(f"  HTTP {status}: {http_status_description(status)}")

    # Сопоставление с несколькими значениями (OR-паттерн)
    def is_weekend(day):
        match day.lower():
            case "суббота" | "воскресенье" | "saturday" | "sunday":
                return True
            case _:
                return False

    print(f"\n  Суббота — выходной? {is_weekend('Суббота')}")
    print(f"  Понедельник — выходной? {is_weekend('Понедельник')}")

    # Продвинутое: сопоставление структур данных
    def process_command(command):
        match command:
            case ["quit" | "exit" | "q"]:
                return "Выход из программы"
            case ["help" | "h"]:
                return "Показать справку"
            case ["greet", name]:
                return f"Привет, {name}!"
            case ["greet", name, age]:
                return f"Привет, {name}! Тебе {age} лет."
            case ["sum", *numbers] if numbers:
                # *numbers — захват оставшихся элементов, if — guard (условие)
                return f"Сумма: {sum(numbers)}"
            case _:
                return f"Неизвестная команда: {command}"

    commands = [
        ["quit"],
        ["help"],
        ["greet", "Анна"],
        ["greet", "Иван", "25"],
        ["sum", 1, 2, 3, 4, 5],
        ["sum"],  # пустой список чисел
        ["unknown", "cmd"],
    ]

    print("\n  Обработка команд:")
    for cmd in commands:
        print(f"    {cmd} → {process_command(cmd)}")

    # Сопоставление словарей
    def handle_event(event):
        match event:
            case {"type": "click", "x": x, "y": y}:
                return f"Клик в точке ({x}, {y})"
            case {"type": "keypress", "key": key}:
                return f"Нажата клавиша: {key}"
            case {"type": "login", "username": user}:
                return f"Вход пользователя: {user}"
            case _:
                return "Неизвестное событие"

    print("\n  Обработка событий:")
    print(f"    {handle_event({'type': 'click', 'x': 100, 'y': 200})}")
    print(f"    {handle_event({'type': 'keypress', 'key': 'Enter'})}")
    print(f"    {handle_event({'type': 'login', 'username': 'admin', 'password': '123'})}")


def demo_truthy_conditions():
    """Использование truthy/falsy значений в условиях."""
    print("\n" + "=" * 50)
    print("📌 TRUTHY / FALSY В УСЛОВИЯХ")
    print("=" * 50)

    # В Python любое значение можно использовать как условие
    # Falsy: None, False, 0, 0.0, "", [], {}, set(), ()
    # Truthy: всё остальное

    def check_value(val):
        if val:
            print(f"  '{val}' ({type(val).__name__}) → True (truthy)")
        else:
            print(f"  '{val}' ({type(val).__name__}) → False (falsy)")

    test_values = [True, False, None, 0, 0.0, 1, -1, "", "hello", [], [1, 2], {}, {"a": 1}]
    for v in test_values:
        check_value(v)

    # Практические паттерны
    print("\n--- Практические паттерны ---")

    # Проверка на пустой список
    items = []
    if not items:
        print("  Список пуст — нечего обрабатывать")
    else:
        print(f"  Обрабатываем {len(items)} элементов")

    # Проверка на наличие значения
    name = ""
    display_name = name or "Аноним"  # Если name пустой — берём "Аноним"
    print(f"  display_name = '{display_name}'")

    name = "Анна"
    display_name = name or "Аноним"
    print(f"  display_name = '{display_name}'")

    # Безопасный доступ к вложенным данным
    config = {}
    timeout = config.get("timeout") or 30  # Если None или 0 или пусто — 30
    print(f"  timeout = {timeout}")


def demo_practical():
    """Практические примеры использования условий."""
    print("\n" + "=" * 50)
    print("📌 ПРАКТИЧЕСКИЕ ПРИМЕРЫ")
    print("=" * 50)

    # Валидация ввода
    def validate_age(age):
        if not isinstance(age, (int, float)):
            return "Ошибка: возраст должен быть числом"
        if age < 0:
            return "Ошибка: возраст не может быть отрицательным"
        if age > 150:
            return "Ошибка: нереалистичный возраст"
        if age < 18:
            return "Доступ запрещён: вам нет 18"
        return "Доступ разрешён"

    for test_age in ["abc", -5, 200, 16, 25]:
        result = validate_age(test_age) if isinstance(test_age, (int, float)) else validate_age(test_age)
        print(f"  Возраст {test_age}: {result}")

    # Калькулятор скидки
    def calculate_discount(amount, is_vip, has_coupon):
        discount = 0
        if amount > 10000:
            discount += 10
        if is_vip:
            discount += 15
        if has_coupon:
            discount += 5
        if discount > 30:
            discount = 30  # Максимальная скидка
        return discount

    print(f"\n  Скидка (5000, не VIP, без купона): {calculate_discount(5000, False, False)}%")
    print(f"  Скидка (15000, VIP, с купоном): {calculate_discount(15000, True, True)}%")


def main():
    """Главная функция."""
    print("🐍 УРОК 05: УСЛОВНЫЕ ОПЕРАТОРЫ")
    print("=" * 50)

    demo_if_else()
    demo_ternary()
    demo_match_case()
    demo_truthy_conditions()
    demo_practical()

    print("\n" + "=" * 50)
    print("✅ Урок 05 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. if/elif/else — множественный выбор условий")
    print("  2. Тернарный оператор: x if cond else y")
    print("  3. match/case (3.10+) — мощное сопоставление с образцом")
    print("  4. Пустые коллекции и None — falsy, используйте в условиях")
    print("=" * 50)


if __name__ == "__main__":
    main()
