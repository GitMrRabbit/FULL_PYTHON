"""
Урок 24: Регулярные выражения (Regex) в Python
===============================================

Темы:
  - re.search(), re.match(), re.findall(), re.finditer()
  - re.sub(), re.split()
  - Группы захвата (capturing groups)
  - Именованные группы (?P<name>...)
  - Флаги: re.IGNORECASE, re.MULTILINE, re.DOTALL, re.VERBOSE
  - Компиляция: re.compile()
  - Жадные и ленивые квантификаторы
"""

import re


# =============================================================================
# 1. БАЗОВЫЕ ФУНКЦИИ
# =============================================================================

def basic_regex_demo():
    """Демонстрация базовых функций re."""
    print("=" * 60)
    print("1. БАЗОВЫЕ ФУНКЦИИ")
    print("=" * 60)

    text = "The price is $19.99. Contact: alice@example.com, +7 (999) 123-45-67"

    # search — первое совпадение (в любом месте)
    match = re.search(r"\$\d+\.\d{2}", text)
    if match:
        print(f"search: {match.group()} at {match.span()}")

    # match — только в начале строки
    m = re.match(r"The", text)
    print(f"match 'The': {'Yes' if m else 'No'}")

    # findall — все совпадения (список строк)
    words = re.findall(r"\b\w{5}\b", text)
    print(f"findall (5-буквенные слова): {words}")

    # finditer — все совпадения (итератор match-объектов)
    print("finditer (слова из 5+ букв):", end=" ")
    for m in re.finditer(r"\b\w{5,}\b", text):
        print(m.group(), end=" ")
    print()

    # sub — замена
    masked = re.sub(r"\d", "X", text)
    print(f"sub (цифры→X): {masked}")

    # split — разделение
    parts = re.split(r"[,.]", text)
    print(f"split по [,.] : {parts}")


# =============================================================================
# 2. ГРУППЫ ЗАХВАТА
# =============================================================================

def groups_demo():
    """Демонстрация групп захвата."""
    print("\n" + "=" * 60)
    print("2. ГРУППЫ ЗАХВАТА")
    print("=" * 60)

    # Обычные группы (numbered groups)
    email = "alice@example.com"
    match = re.search(r"(\w+)@(\w+)\.(\w+)", email)
    if match:
        print(f"Весь email: {match.group(0)}")  # Всё совпадение
        print(f"  user:   {match.group(1)}")     # (\w+)
        print(f"  domain: {match.group(2)}")     # (\w+)
        print(f"  tld:    {match.group(3)}")     # (\w+)
        print(f"  groups: {match.groups()}")     # Все группы кортежем

    # Именованные группы (?P<name>...)
    phone = "+7 (999) 123-45-67"
    pattern = r"\+(?P<country>\d+)\s*\((?P<code>\d+)\)\s*(?P<number>[\d-]+)"
    match = re.search(pattern, phone)
    if match:
        print(f"\nТелефон: {match.group()}")
        print(f"  country: {match.group('country')}")
        print(f"  code:    {match.group('code')}")
        print(f"  number:  {match.group('number')}")
        print(f"  groupdict: {match.groupdict()}")

    # Ссылки на группы (\1, \2) — поиск повторений
    text = "Hello Hello World World"
    duplicates = re.findall(r"\b(\w+)\s+\1\b", text)
    print(f"\nПовторяющиеся слова: {duplicates}")

    # Группы в sub
    date_str = "2024-06-15"
    reformatted = re.sub(r"(\d{4})-(\d{2})-(\d{2})",
                         r"\3.\2.\1", date_str)
    print(f"Дата reformatted: {date_str} → {reformatted}")


# =============================================================================
# 3. ФЛАГИ И КОМПИЛЯЦИЯ
# =============================================================================

def flags_and_compile_demo():
    """Демонстрация флагов и компиляции."""
    print("\n" + "=" * 60)
    print("3. ФЛАГИ И КОМПИЛЯЦИЯ")
    print("=" * 60)

    text = """First line
SECOND LINE
third line"""

    # re.IGNORECASE (re.I) — игнорировать регистр
    matches = re.findall(r"second", text, re.IGNORECASE)
    print(f"IGNORECASE: {matches}")

    # re.MULTILINE (re.M) — ^ и $ на каждой строке
    lines_starting = re.findall(r"^\w+", text, re.MULTILINE)
    print(f"MULTILINE (^): {lines_starting}")

    # re.DOTALL (re.S) — . включает \n
    text_with_newlines = "Hello\nWorld"
    dot_match = re.search(r"Hello.World", text_with_newlines, re.DOTALL)
    print(f"DOTALL: {'Yes' if dot_match else 'No'}")

    # re.VERBOSE (re.X) — читаемые паттерны с комментариями
    email_pattern = re.compile(r"""
        ^                       # Начало строки
        [a-zA-Z0-9._%+-]+      # Имя пользователя
        @                       # @
        [a-zA-Z0-9.-]+         # Домен
        \.                     # Точка
        [a-zA-Z]{2,}$          # TLD (2+ буквы)
    """, re.VERBOSE | re.IGNORECASE)

    test_emails = ["alice@example.com", "bad-email", "bob@company.co.uk"]
    for e in test_emails:
        valid = "✓" if email_pattern.match(e) else "✗"
        print(f"  {valid} {e}")


# =============================================================================
# 4. ЖАДНЫЕ И ЛЕНИВЫЕ КВАНТИФИКАТОРЫ
# =============================================================================

def greedy_vs_lazy_demo():
    """Демонстрация жадных vs ленивых квантификаторов."""
    print("\n" + "=" * 60)
    print("4. ЖАДНЫЕ vs ЛЕНИВЫЕ КВАНТИФИКАТОРЫ")
    print("=" * 60)

    html = "<div>First</div><div>Second</div>"

    # Жадный (.*) — берёт максимум
    greedy = re.findall(r"<div>.*</div>", html)
    print(f"Жадный .*:   {greedy}")  # Всё от первого <div> до последнего </div>

    # Ленивый (.*?) — берёт минимум
    lazy = re.findall(r"<div>.*?</div>", html)
    print(f"Ленивый .*?: {lazy}")    # Два отдельных div

    # Квантификаторы
    # *     0+  (жадный)      *?   (ленивый)
    # +     1+  (жадный)      +?   (ленивый)
    # ?     0-1 (жадный)      ??   (ленивый)
    # {n,m} n-m (жадный)      {n,m}? (ленивый)


# =============================================================================
# 5. ПРАКТИЧЕСКИЕ ПРИМЕРЫ
# =============================================================================

class RegexValidator:
    """Коллекция часто используемых валидаторов."""

    # Предкомпилированные паттерны (быстрее многократного использования)
    EMAIL = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    PHONE_RU = re.compile(r"^\+7\s*\(?\d{3}\)?\s*\d{3}[- ]?\d{2}[- ]?\d{2}$")
    URL = re.compile(
        r"^https?://"                       # Протокол
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # Домен
        r"localhost|"                       # Или localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # Или IP
        r"(?::\d+)?"                        # Порт
        r"(?:/?|[/?]\S+)$", re.IGNORECASE | re.VERBOSE
    )
    IPV4 = re.compile(
        r"^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}"
        r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$"
    )

    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        return bool(cls.EMAIL.match(email))

    @classmethod
    def is_valid_phone_ru(cls, phone: str) -> bool:
        return bool(cls.PHONE_RU.match(phone))

    @classmethod
    def extract_emails(cls, text: str) -> list[str]:
        return cls.EMAIL.findall(text)

    @classmethod
    def extract_urls(cls, text: str) -> list[str]:
        return cls.URL.findall(text)


def practical_demo():
    """Практические примеры использования regex."""
    print("\n" + "=" * 60)
    print("5. ПРАКТИЧЕСКИЕ ПРИМЕРЫ")
    print("=" * 60)

    # Валидация
    print("Валидация:")
    tests = [
        ("email", "alice@example.com", RegexValidator.is_valid_email),
        ("email", "bad-email", RegexValidator.is_valid_email),
        ("phone", "+7 (999) 123-45-67", RegexValidator.is_valid_phone_ru),
        ("phone", "8-800-555-35-35", RegexValidator.is_valid_phone_ru),
        ("ipv4", "192.168.1.1", lambda x: bool(RegexValidator.IPV4.match(x))),
        ("ipv4", "256.0.0.1", lambda x: bool(RegexValidator.IPV4.match(x))),
    ]
    for tag, value, validator in tests:
        status = "✓" if validator(value) else "✗"
        print(f"  {status} {tag:5s}: {value}")

    # Извлечение
    text = "Contact: alice@example.com and bob@company.org. "
    "Visit https://example.com or http://test.org:8080/path"
    emails = RegexValidator.extract_emails(text)
    urls = RegexValidator.extract_urls(text)
    print(f"\nИзвлечённые email: {emails}")
    print(f"Извлечённые URL:   {urls}")


# =============================================================================
# ШПАРГАЛКА ПО СИНТАКСИСУ
# =============================================================================

REGEX_CHEATSHEET = r"""
╔══════════════════════════════════════════════════════════════════╗
║  СИМВОЛ     ОПИСАНИЕ                  ПРИМЕР                    ║
╠══════════════════════════════════════════════════════════════════╣
║  .          Любой символ кроме \n      h.t → hat, hot, h3t      ║
║  \d         Цифра [0-9]                \d+ → 123                 ║
║  \D         НЕ цифра                    \D+ → abc                ║
║  \w         Буква/цифра/_ [a-zA-Z0-9_]  \w+ → hello_world1      ║
║  \W         НЕ буква/цифра/_            \W+ → @#$                ║
║  \s         Пробельный символ            \s+ → '   '             ║
║  \S         НЕ пробельный символ         \S+ → hello             ║
║  \b         Граница слова                \bcat\b → cat, не cats   ║
║  ^          Начало строки                ^Hello                  ║
║  $          Конец строки                 world$                  ║
║  *          0+ раз                       a* → '', a, aa, aaa     ║
║  +          1+ раз                       a+ → a, aa, aaa         ║
║  ?          0-1 раз                      a? → '', a              ║
║  {n}        Ровно n раз                  \d{3} → 123             ║
║  {n,}       n+ раз                       \d{2,} → 12, 12345     ║
║  {n,m}      n-m раз                      \d{2,4} → 12, 1234     ║
║  [abc]      Один из a,b,c                [aeiou] → гласные       ║
║  [^abc]     НЕ a,b,c                     [^0-9] → не цифры       ║
║  [a-z]      Диапазон                     [A-Za-z] → буквы        ║
║  (abc|def)  ИЛИ                          cat|dog → cat или dog   ║
║  (...)      Группа захвата               (\d+)\.(\d+)            ║
║  (?:...)    Не-захватывающая группа       (?:www\.)?             ║
║  (?P<n>...) Именованная группа            (?P<year>\d{4})        ║
║  \1, \2     Ссылка на группу №            (\w+)\s+\1 → дубликат  ║
║  (?=...)    Опережающая проверка          \w+(?=\.com)           ║
║  (?!...)    Отрицательная опережающая     \d+(?!\.)              ║
║  (?<=...)   Ретроспективная проверка      (?<=@)\w+              ║
║  (?<!...)   Отрицательная ретроспективная (?<!-)\d+             ║
╚══════════════════════════════════════════════════════════════════╝
"""


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    basic_regex_demo()
    groups_demo()
    flags_and_compile_demo()
    greedy_vs_lazy_demo()
    practical_demo()

    print("\n" + REGEX_CHEATSHEET)

    print("\n" + "=" * 60)
    print("✅ УРОК 24 ЗАВЕРШЁН: РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ ОСВОЕНЫ!")
    print("=" * 60)
