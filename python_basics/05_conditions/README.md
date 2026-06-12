# 🔀 Урок 05: Условные конструкции в Python

## 📖 Теория

Условные конструкции позволяют программе принимать решения и выполнять разный код в зависимости от условий.

---

## 🔹 `if` / `elif` / `else`

```python
if условие1:
    # Выполняется, если условие1 истинно
    блок_кода1
elif условие2:
    # Выполняется, если условие1 ложно, а условие2 истинно
    блок_кода2
elif условие3:
    # Можно сколько угодно elif
    блок_кода3
else:
    # Выполняется, если все предыдущие условия ложны
    блок_кода4
```

**Пример:**
```python
age = 25

if age < 13:
    print("Ребёнок")
elif age < 18:
    print("Подросток")
elif age < 65:
    print("Взрослый")
else:
    print("Пенсионер")
```

---

## 🎯 Тернарный оператор (однострочный `if/else`)

```python
# Синтаксис: значение_если_True if условие else значение_если_False
status = "Совершеннолетний" if age >= 18 else "Несовершеннолетний"

# Можно использовать в f-строках
print(f"Доступ: {'разрешён' if is_admin else 'запрещён'}")

# Вложенные тернарные (читайте осторожно!)
emoji = "😄" if mood == "happy" else "😢" if mood == "sad" else "😐"
```

---

## 🆕 `match` / `case` (Python 3.10+)

Структурное сопоставление с образцом — мощная замена цепочкам `if/elif`:

```python
def handle_command(command: str):
    match command.split():
        case ["quit"]:
            print("Выход...")
            return True
        case ["help"]:
            print("Доступные команды: ...")
        case ["echo", *words]:
            print(" ".join(words))
        case ["add", x, y]:
            print(f"{x} + {y} = {int(x) + int(y)}")
        case _:                    # default (wildcard)
            print(f"Неизвестная команда: {command}")
    return False
```

**Продвинутые возможности `match/case`:**

```python
# Сопоставление по типу и значению
def process(value):
    match value:
        case int(n) if n > 0:       # Положительное целое
            print(f"Положительное: {n}")
        case int(n) if n < 0:       # Отрицательное целое
            print(f"Отрицательное: {n}")
        case str(s):                 # Любая строка
            print(f"Строка: '{s}'")
        case [*items]:               # Любой список
            print(f"Список из {len(items)} элементов")
        case {"name": name, "age": int(age)}:  # Словарь с ключами
            print(f"{name}, {age} лет")
        case _:
            print("Неизвестный тип")
```

```python
# Сопоставление объектов
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

def locate(point):
    match point:
        case Point(x=0, y=0):
            print("Начало координат")
        case Point(x=0, y=y):
            print(f"Ось Y в точке y={y}")
        case Point(x=x, y=0):
            print(f"Ось X в точке x={x}")
        case Point(x=x, y=y):
            print(f"Точка ({x}, {y})")
```

---

## ⚡ Короткое замыкание (short-circuit)

```python
# Безопасная проверка: если a ложно, b не вычисляется
if a and expensive_operation():
    ...

# Значение по умолчанию через or
name = user_input or "Аноним"

# Безопасный доступ к атрибуту
if obj and obj.method():
    ...
```

---

## 📊 Таблица истинности

| A | B | A and B | A or B | not A |
|---|---|---------|--------|-------|
| True | True | True | True | False |
| True | False | False | True | False |
| False | True | False | True | True |
| False | False | False | False | True |

---

## ⚠️ Частые ошибки

```python
# ❌ Присваивание (=) вместо сравнения (==)
if x = 5:       # SyntaxError!
if x == 5:      # ✅ Правильно

# ❌ Неправильная проверка на None
if x == None:   # ❌ Неправильно
if x is None:   # ✅ Правильно

# ❌ Сравнение с True/False
if flag == True:        # Избыточно
if flag:                # ✅ Достаточно

# ❌ Путаница с and/or в сложных условиях
if x > 0 or x < 10:     # Всегда True! (любое число подходит)
if 0 < x < 10:          # ✅ Правильно: цепочка сравнений
```

---

## 💡 Лучшие практики

1. **Проверяйте наиболее вероятные условия первыми** для производительности
2. **Избегайте глубокой вложенности** (>3 уровней) — выносите в функции или используйте guard clauses
3. **Используйте `match/case`** для сложного сопоставления с образцом (Python 3.10+)
4. **Guard clauses** — возвращайтесь рано вместо вложенных if:
```python
# ❌ Плохо
def process(data):
    if data:
        if data.is_valid():
            if data.is_ready():
                return data.result()

# ✅ Хорошо (guard clauses)
def process(data):
    if not data:
        return None
    if not data.is_valid():
        return None
    if not data.is_ready():
        return None
    return data.result()
```

---

## 🧪 Упражнения

1. Напишите функцию `fizzbuzz(n)`, возвращающую "Fizz" если n делится на 3, "Buzz" если на 5, "FizzBuzz" если на оба, иначе str(n)
2. Реализуйте калькулятор с `match/case`, обрабатывающий 4 операции
3. Напишите функцию `is_triangle(a, b, c)` — можно ли из трёх отрезков составить треугольник
4. Создайте классификатор возраста с тернарным оператором в одну строку
