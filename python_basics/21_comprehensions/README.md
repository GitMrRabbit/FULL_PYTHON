# 🧮 Урок 21: Comprehensions (Генераторы коллекций)

## 📖 Теория

Comprehensions — компактный синтаксис для создания коллекций. Быстрее и читаемее циклов.

---

## 🔹 List Comprehension

```python
[elem for item in iterable]
[elem for item in iterable if condition]
[true_val if cond else false_val for item in iterable]

[x**2 for x in range(5)]                      # [0, 1, 4, 9, 16]
[x for x in range(10) if x % 2 == 0]          # [0, 2, 4, 6, 8]
["чёт" if x%2==0 else "нечет" for x in [1,2]] # ['нечет', 'чёт']
```

**Вложенные:** `[(x,y) for x in range(3) for y in range(2)]` — декартово произведение.

---

## 🔹 Dict Comprehension

```python
{k: v for k, v in iterable}
{k: v for k, v in iterable if condition}

{x: x**2 for x in range(5)}    # {0: 0, 1: 1, 2: 4, ...}
{v: k for k, v in d.items()}   # Инвертирование словаря
```

---

## 🔹 Set Comprehension

```python
{elem for item in iterable}

{x**2 for x in range(-3, 4)}   # {0, 1, 4, 9} — только уникальные!
```

---

## 🔹 Generator Expression

```python
(x**2 for x in range(10))      # Ленивый! Не хранит всё в памяти
sum(x**2 for x in range(10**6))# Не создаёт список!
```

---

## 📊 Сравнение

| Тип | Синтаксис | Память | Повтор |
|-----|-----------|--------|--------|
| List | `[...]` | O(n) | ✅ |
| Dict | `{k:v ...}` | O(n) | ✅ |
| Set | `{...}` | O(n) | ✅ |
| Generator | `(...)` | O(1) | ❌ |

---

## 🧪 Упражнения

1. Создайте список всех простых чисел до 100 через comprehension с `all()`
2. Постройте словарь {слово: длина} для списка слов
3. Создайте множество всех гласных букв в тексте
4. Транспонируйте матрицу через вложенный list comprehension
