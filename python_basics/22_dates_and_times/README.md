# 📅 Урок 22: Даты и Время

## 📖 Основные типы

| Тип | Содержит | Пример |
|-----|---------|--------|
| `date` | Год, месяц, день | `date(2024, 12, 31)` |
| `time` | Часы, минуты, секунды | `time(14, 30, 0)` |
| `datetime` | Дата + время | `datetime(2024, 12, 31, 23, 59)` |
| `timedelta` | Разница | `timedelta(days=7, hours=3)` |

---

## 🔹 Создание и текущее время

```python
from datetime import datetime, date, time, timedelta, timezone

now = datetime.now()
today = date.today()
utc_now = datetime.now(timezone.utc)
specific = datetime(2024, 6, 15, 14, 30, 0)
```

---

## 🔹 Форматирование

```python
# datetime → строка (strftime)
dt.strftime("%d.%m.%Y %H:%M:%S")  # "15.06.2024 14:30:00"
dt.strftime("%Y-%m-%dT%H:%M:%S")  # "2024-06-15T14:30:00" (ISO 8601)

# строка → datetime (strptime)
datetime.strptime("15.06.2024", "%d.%m.%Y")
```

**Коды:** `%Y`=год, `%m`=месяц, `%d`=день, `%H`=час, `%M`=минуты, `%S`=секунды, `%A`=день недели.

---

## 🔹 Арифметика дат

```python
tomorrow = today + timedelta(days=1)
last_week = today - timedelta(weeks=1)
diff = date(2025, 1, 1) - today  # timedelta
diff.days  # количество дней
```

---

## 🔹 Часовые пояса (Python 3.9+)

```python
from zoneinfo import ZoneInfo  # Python 3.9+
msk = datetime.now(ZoneInfo("Europe/Moscow"))
ny = datetime.now(ZoneInfo("America/New_York"))
utc_dt.astimezone(ZoneInfo("Europe/Moscow"))
```

---

## 🧪 Упражнения

1. Сколько дней осталось до Нового года?
2. Вычислите свой возраст в днях
3. Выведите все пятницы 13-го в текущем году
4. Напишите конвертер дат между часовыми поясами
