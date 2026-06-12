# 📖 Урок 09: Словари (Dictionaries) в Python

## 📖 Теория

Словарь (`dict`) — неупорядоченная (до Python 3.6) / упорядоченная (Python 3.7+) коллекция пар **ключ-значение**. Ключи должны быть хешируемыми (неизменяемыми).

---

## 🔹 Создание

```python
d = {"name": "Анна", "age": 28, "city": "Москва"}
d = dict(name="Анна", age=28)         # Только строковые ключи
d = dict([("a", 1), ("b", 2)])        # Из списка пар
d = dict.fromkeys(["a", "b", "c"], 0) # {'a': 0, 'b': 0, 'c': 0}
d = {}                                 # Пустой
```

---

## 🔹 Доступ и изменение

```python
d["name"]            # Получить значение (KeyError если нет ключа)
d.get("name")        # Получить значение (None если нет)
d.get("name", "Н/Д") # Со значением по умолчанию
d["new_key"] = 42    # Добавить/обновить

# Безопасное обновление
d.setdefault("count", 0)  # Вернуть значение, если ключ есть, иначе создать с 0
```

---

## 🔹 Методы словарей

```python
d.keys()          # Все ключи (dict_keys — view object)
d.values()        # Все значения
d.items()         # Пары (ключ, значение)

d.pop("key")          # Удалить и вернуть значение
d.popitem()           # Удалить и вернуть последнюю пару (LIFO в 3.7+)
d.update(other_dict)  # Обновить из другого словаря
d.clear()             # Очистить

# Проверки
"key" in d         # Проверка наличия ключа (O(1)!)
"val" in d.values()# Проверка наличия значения (O(n))
```

---

## 🔹 Объединение словарей (Python 3.9+)

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

merged = d1 | d2           # {'a': 1, 'b': 3, 'c': 4} (d2 перезаписывает)
d1 |= d2                   # d1 обновлён: {'a': 1, 'b': 3, 'c': 4}
```

---

## 🔹 Dict Comprehensions

```python
# Базовый синтаксис
{k: v for k, v in [("a", 1), ("b", 2)]}
{k: v * 2 for k, v in d.items()}
{k: v for k, v in d.items() if v > 0}

# Инвертирование словаря
{v: k for k, v in d.items()}

# Из двух списков
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}
```

---

## 🔹 Продвинутые типы словарей (`collections`)

### `defaultdict` — словарь со значением по умолчанию
```python
from collections import defaultdict

# Обычный способ — громоздкий
d = {}
for word in ["a", "b", "a"]:
    if word not in d:
        d[word] = 0
    d[word] += 1

# defaultdict — элегантно
d = defaultdict(int)
for word in ["a", "b", "a"]:
    d[word] += 1  # int() = 0 при первом обращении
# defaultdict(<class 'int'>, {'a': 2, 'b': 1})

# Другие фабрики
defaultdict(list)    # defaultdict(list) — [] по умолчанию
defaultdict(set)     # defaultdict(set)  — set() по умолчанию
defaultdict(lambda: "unknown")
```

### `Counter` — счётчик
```python
from collections import Counter

c = Counter("abracadabra")
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

c.most_common(2)     # [('a', 5), ('b', 2)]
c["a"]               # 5
c["z"]               # 0 (не KeyError!)

c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
c1 + c2              # Counter({'a': 4, 'b': 3})
c1 - c2              # Counter({'a': 2})
c1 & c2              # Пересечение: Counter({'a': 1, 'b': 1})
c1 | c2              # Объединение: Counter({'a': 3, 'b': 2})
```

### `OrderedDict` (Python 3.7+: обычный dict уже упорядочен)
```python
from collections import OrderedDict
# Полезен для: move_to_end(), сравнения с учётом порядка, popitem(last=False)
```

### `ChainMap` — поиск по цепочке словарей
```python
from collections import ChainMap
defaults = {"color": "red", "size": "M"}
user = {"color": "blue"}
combined = ChainMap(user, defaults)
combined["color"]  # "blue" (из user)
combined["size"]   # "M" (из defaults)
```

---

## 🔹 Вложенные словари

```python
users = {
    "alice": {"age": 28, "email": "alice@example.com"},
    "bob":   {"age": 35, "email": "bob@example.com"},
}

# Безопасный доступ к вложенным значениям
users.get("alice", {}).get("email", "N/A")

# defaultdict для вложенных структур
tree = lambda: defaultdict(tree)
root = tree()
root["a"]["b"]["c"] = 123
```

---

## ⚠️ Частые ошибки

```python
# ❌ Изменяемый ключ
d[[1, 2, 3]] = "value"  # TypeError: unhashable type: 'list'

# ❌ Изменение словаря во время итерации
for k in d:
    if condition:
        del d[k]  # RuntimeError!

# ✅ Итерация по копии ключей
for k in list(d):
    if condition:
        del d[k]

# ❌ d.get() возвращает None для отсутствующих ключей
d.get("missing").upper()  # AttributeError: 'NoneType'!

# ✅ Используйте значение по умолчанию
d.get("missing", "").upper()
```

---

## 🧪 Упражнения

1. Напишите функцию `group_by(iterable, key_func)` для группировки элементов по ключу
2. Реализуйте частотный анализ текста с помощью `Counter`
3. Создайте словарь с вложенной структурой для хранения студентов → предметы → оценки
4. Инвертируйте словарь (ключи ↔ значения), корректно обрабатывая дубликаты
