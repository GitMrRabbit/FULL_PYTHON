"""
Ответы к упражнениям уроков 01-09 (Основы синтаксиса)
======================================================

Как использовать:
  python python_basics/answers/lesson_01_09_answers.py

Сначала попробуйте решить САМИ, потом сверяйтесь с ответами.
"""

# =============================================================================
# Урок 01: Hello World
# =============================================================================

# Упражнение 1: Вывести "Я изучаю Python!" тремя разными способами
print("Я изучаю Python!")                     # Способ 1
message = "Я изучаю Python!"
print(message)                                 # Способ 2
print("Я", "изучаю", "Python!")               # Способ 3

# Упражнение 2: Спросить имя и поздороваться
name = input("Как вас зовут? ")
print(f"Привет, {name}! Добро пожаловать в Python!")

# Упражнение 3: Калькулятор двух чисел
a = int(input("Первое число: "))
b = int(input("Второе число: "))
print(f"{a} + {b} = {a + b}")


# =============================================================================
# Урок 02: Переменные и типы
# =============================================================================

# Упражнение 1: Конвертер температур (Цельсий → Фаренгейт)
def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

# Упражнение 2: Вычисление площади круга
import math
def circle_area(radius):
    return math.pi * radius ** 2

# Упражнение 3: Проверка типов разных значений
values = [42, "hello", 3.14, True, None, [1, 2], {"key": "val"}]
for v in values:
    print(f"{v!r:15s} → {type(v).__name__}")


# =============================================================================
# Урок 03: Строки
# =============================================================================

# Упражнение 1: Проверка палиндрома
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

assert is_palindrome("А роза упала на лапу Азора") == True
assert is_palindrome("Python") == False

# Упражнение 2: Подсчёт гласных и согласных
def count_letters(text):
    vowels = "аеёиоуыэюяaeiou"
    v = sum(1 for ch in text.lower() if ch in vowels)
    c = sum(1 for ch in text.lower() if ch.isalpha() and ch not in vowels)
    return v, c

# Упражнение 3: Каждое слово с большой буквы
def capitalize_words(sentence):
    return " ".join(word.capitalize() for word in sentence.split())


# =============================================================================
# Урок 04: Операторы
# =============================================================================

# Упражнение 1: Високосный год
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Упражнение 2: Калькулятор с 4 операциями
def calculator(a, b, op):
    if op == "+": return a + b
    elif op == "-": return a - b
    elif op == "*": return a * b
    elif op == "/": return a / b if b != 0 else "Ошибка: деление на 0"
    else: return "Неизвестная операция"

# Упражнение 3: Проверка степени двойки (побитово)
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


# =============================================================================
# Урок 05: Условия
# =============================================================================

# Упражнение 1: FizzBuzz
def fizzbuzz(n):
    if n % 15 == 0: return "FizzBuzz"
    if n % 3 == 0: return "Fizz"
    if n % 5 == 0: return "Buzz"
    return str(n)

# Упражнение 2: Калькулятор с match/case
def calc_match(a, b, op):
    match op:
        case "+": return a + b
        case "-": return a - b
        case "*": return a * b
        case "/": return a / b if b else "Ошибка"
        case _: return "Неизвестно"

# Упражнение 3: Проверка треугольника
def is_triangle(a, b, c):
    return a + b > c and a + c > b and b + c > a


# =============================================================================
# Урок 06: Циклы
# =============================================================================

# Упражнение 1: Таблица умножения 9x9
def multiplication_table():
    for i in range(1, 10):
        for j in range(1, 10):
            print(f"{i}×{j}={i*j:2d}", end="  ")
        print()

# Упражнение 2: Простые числа до n (Решето Эратосфена)
def find_primes(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]

# Упражнение 3: FizzBuzz от 1 до 100
def fizzbuzz_100():
    return [fizzbuzz(i) for i in range(1, 101)]

# Упражнение 4: Список букв кроме гласных в верхнем регистре
def consonants_upper(text):
    vowels = "aeiouаеёиоуыэюя"
    return [ch.upper() for ch in text if ch.isalpha() and ch.lower() not in vowels]

# Упражнение 5: Игра "Угадай число"
import random
def guess_number():
    target = random.randint(1, 100)
    attempts = 0
    while True:
        guess = int(input("Угадай число (1-100): "))
        attempts += 1
        if guess < target:
            print("Больше!")
        elif guess > target:
            print("Меньше!")
        else:
            print(f"Угадал за {attempts} попыток!")
            break


# =============================================================================
# Урок 07: Списки
# =============================================================================

# Упражнение 1: Удаление дубликатов с сохранением порядка
def remove_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# Упражнение 2: "Сплющивание" вложенных списков
def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Упражнение 3: Транспонирование матрицы
def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

# Упражнение 4: Пересечение двух списков без множеств
def intersection(lst1, lst2):
    return [x for x in lst1 if x in lst2 and x not in lst2[:lst2.index(x)]]


# =============================================================================
# Урок 08: Кортежи и Множества
# =============================================================================

# Упражнение 1: Общие элементы через множества
def common_elements(lst1, lst2):
    return list(set(lst1) & set(lst2))

# Упражнение 2: Удаление дубликатов с сохранением порядка (без set)
def unique_ordered(lst):
    return list(dict.fromkeys(lst))

# Упражнение 3: Student namedtuple и средний балл
from collections import namedtuple
Student = namedtuple("Student", ["name", "age", "grades"])

def average_grade(student):
    return sum(student.grades) / len(student.grades)

# Упражнение 4: Уникальные слова в тексте
import re
def unique_words(text):
    return set(re.findall(r"\w+", text.lower()))


# =============================================================================
# Урок 09: Словари
# =============================================================================

# Упражнение 1: Группировка по ключу
def group_by(iterable, key_func):
    groups = {}
    for item in iterable:
        key = key_func(item)
        groups.setdefault(key, []).append(item)
    return groups

# Упражнение 2: Частотный анализ текста
from collections import Counter
def word_frequency(text):
    words = re.findall(r"\w+", text.lower())
    return Counter(words)

# Упражнение 3: Вложенный словарь (студенты → предметы → оценки)
def student_grades():
    return {
        "Анна": {"математика": 5, "физика": 4, "информатика": 5},
        "Борис": {"математика": 4, "физика": 5, "информатика": 4},
        "Вера": {"математика": 5, "физика": 5, "информатика": 5},
    }

# Упражнение 4: Инвертирование словаря с дубликатами
def invert_dict(d):
    result = {}
    for k, v in d.items():
        result.setdefault(v, []).append(k)
    return result


# =============================================================================
# САМОПРОВЕРКА
# =============================================================================

if __name__ == "__main__":
    print("Проверка ответов к урокам 01-09:\n")

    print(f"is_palindrome('А роза упала на лапу Азора'): {is_palindrome('А роза упала на лапу Азора')}")
    print(f"count_letters('Hello World'): {count_letters('Hello World')}")
    print(f"capitalize_words('hello world'): {capitalize_words('hello world')}")
    print(f"is_leap_year(2024): {is_leap_year(2024)}")
    print(f"fizzbuzz(15): {fizzbuzz(15)}")
    print(f"fizzbuzz(3): {fizzbuzz(3)}")
    print(f"fizzbuzz(5): {fizzbuzz(5)}")
    print(f"find_primes(20): {find_primes(20)}")
    print(f"remove_duplicates([1,2,2,3,1,4]): {remove_duplicates([1,2,2,3,1,4])}")
    print(f"flatten([1,[2,[3,4],5],6]): {flatten([1,[2,[3,4],5],6])}")
    print(f"transpose([[1,2],[3,4]]): {transpose([[1,2],[3,4]])}")
    print(f"unique_words('Hello hello WORLD'): {unique_words('Hello hello WORLD')}")
    print(f"group_by(['cat','dog','cow'], len): {group_by(['cat','dog','cow'], len)}")
    print(f"word_frequency('cat dog cat'): {word_frequency('cat dog cat')}")
    print(f"invert_dict({{'a':1, 'b':1, 'c':2}}): {invert_dict({'a':1, 'b':1, 'c':2})}")

    print("\n✅ Все проверки пройдены!")
