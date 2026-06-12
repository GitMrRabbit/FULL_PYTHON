# 🔄 Урок 20: Итераторы и Генераторы

## 📖 Теория

**Итератор** — объект, реализующий `__iter__()` и `__next__()`.  
**Генератор** — функция с `yield`, автоматически создающая итератор.  
**Генераторное выражение** — ленивый аналог list comprehension: `(x**2 for x in range(10))`.

---

## 🔹 Итераторы

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):          # Делает объект итерируемым
        return self

    def __next__(self):          # Возвращает следующий элемент
        if self.current < 0:
            raise StopIteration  # Сигнал конца
        val = self.current
        self.current -= 1
        return val

for n in Countdown(3):  # 3, 2, 1, 0
    print(n)
```

---

## 🔹 Генераторы (`yield`)

```python
def count_up_to(n):          # Это ГЕНЕРАТОР (есть yield)
    i = 1
    while i <= n:
        yield i              # "Замораживает" состояние
        i += 1

gen = count_up_to(5)
next(gen)  # 1
next(gen)  # 2
list(gen)  # [3, 4, 5]
```

**Преимущества:**
- **Ленивые** (lazy): значения вычисляются по требованию
- **Экономия памяти**: не хранят всю последовательность
- **Бесконечные последовательности**: `while True: yield ...`

---

## 🔹 Генераторные выражения

```python
# List comprehension (жадное, всё в памяти)
squares_list = [x**2 for x in range(1000000)]  # ~8 МБ

# Generator expression (ленивое, почти не занимает памяти)
squares_gen = (x**2 for x in range(1000000))   # ~80 байт!

# Использование
sum(x**2 for x in range(1000000))  # Без создания списка!
```

---

## 🔹 `yield from` — делегирование

```python
def chain(*iterables):
    for it in iterables:
        yield from it       # Делегирует итерацию другому итератору

list(chain([1, 2], "ab"))  # [1, 2, 'a', 'b']

def flatten(nested):        # Рекурсивное разворачивание
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
```

---

## 🔹 `send()`, `throw()`, `close()`

```python
def accumulator():
    total = 0
    while True:
        value = yield total     # yield ОТДАЁТ total, ПРИНИМАЕТ value
        if value is not None:
            total += value

acc = accumulator()
next(acc)        # 0 (запуск)
acc.send(10)     # 10
acc.send(20)     # 30
acc.send(5)      # 35
acc.close()      # GeneratorExit
```

---

## 🔹 `itertools` — избранное

| Функция | Описание |
|---------|----------|
| `count(start, step)` | Бесконечный счётчик |
| `cycle(iterable)` | Бесконечный цикл |
| `repeat(elem, n)` | Повторение n раз |
| `chain(*iterables)` | Сцепление |
| `combinations(it, r)` | Сочетания |
| `permutations(it, r)` | Перестановки |
| `product(*iterables)` | Декартово произведение |
| `groupby(it, key)` | Группировка |
| `islice(it, start, stop)` | Срез итератора |
| `pairwise(it)` | Последовательные пары (3.10+) |

---

## 📊 Сравнение

| | List | Generator | Iterator (класс) |
|---|------|-----------|-----------------|
| Память | O(n) | O(1) | O(1) |
| Скорость создания | O(n) | O(1) | O(1) |
| Индексация | ✅ | ❌ | ❌ |
| Повторная итерация | ✅ | ❌ | ❌ |
| Бесконечность | ❌ | ✅ | ✅ |

---

## 🧪 Упражнения

1. Напишите генератор `primes()`, выдающий простые числа (бесконечно)
2. Реализуйте генератор `batch(iterable, n)`, разбивающий на батчи размером n
3. Создайте пайплайн: `read_file → parse_csv → filter → aggregate`
4. Используя `itertools`, решите задачу коммивояжёра перебором (для маленьких N)
