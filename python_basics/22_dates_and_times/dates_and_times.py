"""
Урок 22: Даты и Время в Python
===============================

Темы:
  - datetime: date, time, datetime, timedelta
  - Форматирование: strftime / strptime
  - Часовые пояса: timezone, pytz (zoneinfo в 3.9+)
  - Работа с временными метками: timestamp
  - Арифметика дат: timedelta
  - calendar — календари
  - Лучшие практики
"""

from datetime import datetime, date, time, timedelta, timezone
import calendar
import time as _time


# =============================================================================
# 1. БАЗОВЫЕ ТИПЫ
# =============================================================================

def basic_types_demo():
    """Демонстрация базовых типов datetime."""
    print("=" * 60)
    print("1. БАЗОВЫЕ ТИПЫ")
    print("=" * 60)

    # date — только дата
    d = date(2024, 12, 31)
    print(f"date: {d}")
    print(f"  year={d.year}, month={d.month}, day={d.day}")
    print(f"  weekday()={d.weekday()} (0=Пн), isoweekday()={d.isoweekday()} (1=Пн)")

    # time — только время
    t = time(14, 30, 45, 500_000)  # 14:30:45.500000
    print(f"\ntime: {t}")
    print(f"  hour={t.hour}, minute={t.minute}, second={t.second}, microsecond={t.microsecond}")

    # datetime — дата + время
    dt = datetime(2024, 12, 31, 23, 59, 59)
    print(f"\ndatetime: {dt}")
    print(f"  date()={dt.date()}, time()={dt.time()}")

    # timedelta — разница между датами/временем
    delta = timedelta(days=7, hours=3, minutes=30)
    print(f"\ntimedelta: {delta}")
    print(f"  days={delta.days}, seconds={delta.seconds}, total_seconds()={delta.total_seconds()}")

    # Сейчас
    now = datetime.now()
    today = date.today()
    print(f"\nСейчас: {now}")
    print(f"Сегодня: {today}")


# =============================================================================
# 2. ФОРМАТИРОВАНИЕ (strftime / strptime)
# =============================================================================

def formatting_demo():
    """Демонстрация strftime и strptime."""
    print("\n" + "=" * 60)
    print("2. ФОРМАТИРОВАНИЕ")
    print("=" * 60)

    dt = datetime(2024, 6, 15, 14, 30, 0)

    # strftime: datetime → строка
    formats = {
        "%Y-%m-%d": "%Y-%m-%d (ISO date)",
        "%d.%m.%Y": "%d.%m.%Y (русский)",
        "%H:%M:%S": "%H:%M:%S (24h)",
        "%I:%M %p": "%I:%M %p (12h AM/PM)",
        "%A, %d %B %Y": "%A, %d %B %Y (полный)",
        "%d %b %y": "%d %b %y (сокращённый)",
        "%Y-%m-%dT%H:%M:%S": "%Y-%m-%dT%H:%M:%S (ISO 8601)",
    }

    print("strftime (datetime → строка):")
    for fmt, desc in formats.items():
        print(f"  {desc:25s} → {dt.strftime(fmt)}")

    # strptime: строка → datetime
    print("\nstrptime (строка → datetime):")
    examples = [
        ("2024-06-15", "%Y-%m-%d"),
        ("15.06.2024", "%d.%m.%Y"),
        ("15/06/2024 14:30:00", "%d/%m/%Y %H:%M:%S"),
        ("2024-06-15T14:30:00Z", "%Y-%m-%dT%H:%M:%SZ"),
    ]
    for s, fmt in examples:
        parsed = datetime.strptime(s, fmt)
        print(f"  {s:25s} ({fmt:20s}) → {parsed}")

    # Спецификаторы:
    # %Y — год (4 цифры), %y — год (2 цифры)
    # %m — месяц (01-12), %B — название месяца, %b — сокр.
    # %d — день (01-31)
    # %H — час (00-23), %I — час (01-12), %p — AM/PM
    # %M — минуты, %S — секунды, %f — микросекунды
    # %A — день недели, %a — сокр. день недели
    # %j — день года (001-366)
    # %W — номер недели в году


# =============================================================================
# 3. АРИФМЕТИКА ДАТ (timedelta)
# =============================================================================

def date_arithmetic_demo():
    """Демонстрация арифметики дат."""
    print("\n" + "=" * 60)
    print("3. АРИФМЕТИКА ДАТ (timedelta)")
    print("=" * 60)

    today = date.today()

    # +/- timedelta
    print(f"Сегодня:         {today}")
    print(f"+ 7 дней:         {today + timedelta(days=7)}")
    print(f"- 30 дней:        {today - timedelta(days=30)}")
    print(f"+ 1 год (~365д):  {today + timedelta(days=365)}")

    # Разница между датами
    new_year = date(today.year + 1, 1, 1)
    days_left = (new_year - today).days
    print(f"\nДо Нового года: {days_left} дней")

    # Вычисление возраста
    birth = date(1995, 5, 15)
    age_days = (today - birth).days
    age_years = age_days // 365
    print(f"Возраст (р. {birth}): {age_years} лет ({age_days} дней)")

    # Временные интервалы
    start = datetime.now()
    # ... какой-то код ...
    _time.sleep(0.01)  # Имитация работы
    end = datetime.now()
    elapsed = end - start
    print(f"\nЗамер времени: {elapsed.total_seconds():.4f} сек")


# =============================================================================
# 4. ЧАСОВЫЕ ПОЯСА (timezone)
# =============================================================================

def timezone_demo():
    """Демонстрация часовых поясов."""
    print("\n" + "=" * 60)
    print("4. ЧАСОВЫЕ ПОЯСА")
    print("=" * 60)

    # UTC
    utc_now = datetime.now(timezone.utc)
    print(f"UTC сейчас: {utc_now}")

    # Фиксированное смещение
    msk_tz = timezone(timedelta(hours=3))  # UTC+3 (Москва)
    msk_now = datetime.now(msk_tz)
    print(f"МСК сейчас: {msk_now}")

    # Конвертация между зонами
    ny_tz = timezone(timedelta(hours=-4))  # UTC-4 (Нью-Йорк, летнее)
    ny_now = utc_now.astimezone(ny_tz)
    print(f"Нью-Йорк сейчас: {ny_now}")

    # timestamp — секунды с 01.01.1970 (Unix Epoch)
    ts = datetime.now().timestamp()
    print(f"\ntimestamp: {ts}")
    dt_from_ts = datetime.fromtimestamp(ts)
    print(f"Из timestamp: {dt_from_ts}")

    # ISO 8601
    iso_str = datetime.now(timezone.utc).isoformat()
    print(f"\nISO 8601: {iso_str}")


# =============================================================================
# 5. CALENDAR — КАЛЕНДАРИ
# =============================================================================

def calendar_demo():
    """Демонстрация модуля calendar."""
    print("\n" + "=" * 60)
    print("5. CALENDAR")
    print("=" * 60)

    # Текстовый календарь на месяц
    print("Июнь 2024:")
    print(calendar.month(2024, 6))

    # Проверка високосного года
    print(f"2024 — високосный: {calendar.isleap(2024)}")
    print(f"2023 — високосный: {calendar.isleap(2023)}")

    # День недели (0=Пн)
    print(f"\n01.01.2024 — день недели: {calendar.day_name[calendar.weekday(2024, 1, 1)]}")

    # Календарь на год (первые 3 месяца)
    print("\nПервые 3 месяца 2024:")
    print(calendar.TextCalendar(calendar.MONDAY).formatyear(2024, m=3))


# =============================================================================
# 6. ПРАКТИЧЕСКИЙ ПРИМЕР: ПЛАНИРОВЩИК
# =============================================================================

class TaskScheduler:
    """Планировщик задач с учётом рабочих дней."""

    WEEKEND_DAYS = {5, 6}  # Сб, Вс (0=Пн)

    def __init__(self):
        self._tasks: list[tuple[str, datetime]] = []

    def add_task(self, name: str, deadline: datetime) -> None:
        self._tasks.append((name, deadline))

    def get_upcoming(self, days: int = 7) -> list[tuple[str, datetime]]:
        """Задачи на ближайшие N дней."""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        return [(n, d) for n, d in self._tasks if now <= d <= cutoff]

    def add_business_days(self, dt: datetime, days: int) -> datetime:
        """Добавить N рабочих дней (пропуская выходные)."""
        current = dt
        added = 0
        while added < days:
            current += timedelta(days=1)
            if current.weekday() not in self.WEEKEND_DAYS:
                added += 1
        return current

    def is_business_day(self, dt: datetime) -> bool:
        return dt.weekday() not in self.WEEKEND_DAYS

    @staticmethod
    def format_deadline(dt: datetime) -> str:
        """Форматирование крайнего срока."""
        now = datetime.now()
        diff = dt - now
        if diff.days < 0:
            return f"ПРОСРОЧЕНО ({abs(diff.days)} дн.)"
        elif diff.days == 0:
            hours = diff.seconds // 3600
            return f"СЕГОДНЯ (через {hours} ч)"
        elif diff.days == 1:
            return "ЗАВТРА"
        else:
            return f"через {diff.days} дн."


def practical_example():
    """Практический пример: планировщик задач."""
    print("\n" + "=" * 60)
    print("6. ПРАКТИЧЕСКИЙ ПРИМЕР: ПЛАНИРОВЩИК")
    print("=" * 60)

    scheduler = TaskScheduler()
    now = datetime.now()

    scheduler.add_task("Сдать отчёт", now + timedelta(days=2))
    scheduler.add_task("Ревью кода", now + timedelta(hours=5))
    scheduler.add_task("Релиз", scheduler.add_business_days(now, 5))

    print("Ближайшие задачи:")
    for name, deadline in scheduler.get_upcoming(14):
        print(f"  [{scheduler.format_deadline(deadline)}] {name} — {deadline.strftime('%d.%m.%Y %H:%M')}")

    print(f"\nЧерез 5 рабочих дней: {scheduler.add_business_days(now, 5).strftime('%d.%m.%Y')}")


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    basic_types_demo()
    formatting_demo()
    date_arithmetic_demo()
    timezone_demo()
    calendar_demo()
    practical_example()

    print("\n" + "=" * 60)
    print("✅ УРОК 22 ЗАВЕРШЁН: ДАТЫ И ВРЕМЯ ОСВОЕНЫ!")
    print("=" * 60)
