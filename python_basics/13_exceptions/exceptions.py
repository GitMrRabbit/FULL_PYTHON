"""
УРОК 13: Исключения (try/except/else/finally)
===============================================

Демонстрирует:
- try/except — перехват ошибок
- else — код при отсутствии исключений
- finally — код, выполняемый всегда
- raise — возбуждение исключения
- Создание пользовательских исключений
- Контекстные менеджеры (with)
"""


def demo_try_except():
    """Базовый перехват исключений."""
    print("=" * 50)
    print("📌 TRY / EXCEPT — ОСНОВЫ")
    print("=" * 50)

    # Простой перехват
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"❌ Перехвачено: {type(e).__name__}: {e}")

    # Перехват нескольких типов исключений
    def safe_convert(value):
        try:
            return int(value)
        except ValueError:
            return f"'{value}' не является числом"
        except TypeError:
            return f"Тип {type(value).__name__} нельзя конвертировать в int"

    print(f"\nsafe_convert('123'): {safe_convert('123')}")
    print(f"safe_convert('abc'): {safe_convert('abc')}")
    print(f"safe_convert(None): {safe_convert(None)}")

    # Перехват нескольких в одном except
    def divide(a, b):
        try:
            return a / b
        except (ZeroDivisionError, TypeError) as e:
            return f"Ошибка: {e}"

    print(f"\ndivide(10, 2): {divide(10, 2)}")
    print(f"divide(10, 0): {divide(10, 0)}")
    print(f"divide(10, 'a'): {divide(10, 'a')}")


def demo_else_finally():
    """else и finally."""
    print("\n" + "=" * 50)
    print("📌 else, finally")
    print("=" * 50)

    # else — выполняется, если исключений НЕ было
    def read_file_safely(filename):
        try:
            f = open(filename, 'r', encoding='utf-8')
        except FileNotFoundError:
            print(f"❌ Файл '{filename}' не найден")
        else:
            content = f.read()
            f.close()
            print(f"✅ Файл '{filename}' прочитан ({len(content)} символов)")
            return content
        finally:
            print(f"   [finally: попытка чтения '{filename}' завершена]")

    # Существующий файл
    read_file_safely("python_basics/01_hello_world/main.py")
    print()
    # Несуществующий файл
    read_file_safely("nonexistent.txt")

    # finally ВСЕГДА выполняется — даже при return или исключении!
    def demo_finally():
        try:
            print("   try: начинаем")
            return "возвращаем из try"
        finally:
            print("   finally: выполняется в ЛЮБОМ случае!")

    print(f"\nРезультат: {demo_finally()}")


def demo_raise():
    """raise — возбуждение исключений."""
    print("\n" + "=" * 50)
    print("📌 raise")
    print("=" * 50)

    def validate_age(age):
        if not isinstance(age, int):
            raise TypeError(f"Возраст должен быть int, а не {type(age).__name__}")
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным!")
        if age > 150:
            raise ValueError(f"Возраст {age} нереалистичен!")
        return f"Возраст {age} валиден"

    for test in [25, -5, "abc", 200]:
        try:
            print(f"  validate_age({test}): {validate_age(test)}")
        except (TypeError, ValueError) as e:
            print(f"  validate_age({test}): ❌ {e}")

    # raise from — цепочка исключений
    def process_data(raw):
        try:
            value = int(raw)
        except ValueError as original_error:
            raise ValueError(f"Не удалось обработать '{raw}'") from original_error

    try:
        process_data("abc")
    except ValueError as e:
        print(f"\nЦепочка исключений: {e}")
        print(f"  Исходное: {e.__cause__}")


def demo_custom_exceptions():
    """Создание пользовательских исключений."""
    print("\n" + "=" * 50)
    print("📌 ПОЛЬЗОВАТЕЛЬСКИЕ ИСКЛЮЧЕНИЯ")
    print("=" * 50)

    class InsufficientFundsError(Exception):
        """Недостаточно средств на счёте."""
        def __init__(self, balance, amount):
            self.balance = balance
            self.amount = amount
            super().__init__(
                f"Недостаточно средств: баланс {balance}, "
                f"требуется {amount}, не хватает {amount - balance}"
            )

    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def withdraw(self, amount):
            if amount <= 0:
                raise ValueError("Сумма снятия должна быть положительной")
            if amount > self.balance:
                raise InsufficientFundsError(self.balance, amount)
            self.balance -= amount
            return self.balance

        def deposit(self, amount):
            if amount <= 0:
                raise ValueError("Сумма пополнения должна быть положительной")
            self.balance += amount
            return self.balance

    account = BankAccount("Анна", 1000)

    try:
        account.withdraw(1500)
    except InsufficientFundsError as e:
        print(f"❌ {e}")
        print(f"   Баланс: {e.balance}, Требуется: {e.amount}")

    account.deposit(500)
    print(f"Пополнили 500, баланс: {account.balance}")
    account.withdraw(300)
    print(f"Сняли 300, баланс: {account.balance}")

    # Иерархия исключений
    class AppError(Exception):
        """Базовое исключение приложения."""

    class DatabaseError(AppError):
        """Ошибка базы данных."""

    class NetworkError(AppError):
        """Ошибка сети."""

    # Перехват по базовому классу
    try:
        raise DatabaseError("Соединение с БД потеряно")
    except AppError as e:
        print(f"\nПерехват по базовому классу: {type(e).__name__}: {e}")


def demo_context_managers():
    """Контекстные менеджеры (with)."""
    print("\n" + "=" * 50)
    print("📌 КОНТЕКСТНЫЕ МЕНЕДЖЕРЫ (with)")
    print("=" * 50)

    # with автоматически вызывает __enter__ и __exit__
    # Гарантирует закрытие ресурсов даже при исключении!

    # Работа с файлами
    print("--- with для файлов ---")
    try:
        with open("python_basics/01_hello_world/main.py", "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        print(f"  Первая строка: '{first_line}'")
        print(f"  Файл закрыт? {f.closed}")  # True!
    except FileNotFoundError:
        pass

    # Свой контекстный менеджер через класс
    class Timer:
        """Замеряет время выполнения блока."""
        def __enter__(self):
            import time
            self.start = time.perf_counter()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            import time
            self.end = time.perf_counter()
            self.elapsed = self.end - self.start
            if exc_type:
                print(f"  [Timer] Ошибка: {exc_type.__name__}")
            return False  # Не подавляем исключение

    with Timer() as timer:
        total = sum(range(1000000))
    print(f"  Сумма 1M чисел: {total}")
    print(f"  Время: {timer.elapsed:.4f} сек")

    # Свой контекстный менеджер через contextlib
    from contextlib import contextmanager

    @contextmanager
    def managed_resource(name):
        print(f"  🔓 Открываем {name}...")
        try:
            yield f"resource:{name}"  # то, что попадёт в as
        finally:
            print(f"  🔒 Закрываем {name}...")

    with managed_resource("DB_Connection") as conn:
        print(f"  Работаем с {conn}")


def main():
    """Главная функция."""
    print("🐍 УРОК 13: ИСКЛЮЧЕНИЯ")
    print("=" * 50)

    demo_try_except()
    demo_else_finally()
    demo_raise()
    demo_custom_exceptions()
    demo_context_managers()

    print("\n" + "=" * 50)
    print("✅ Урок 13 завершён!")
    print("📝 Ключевые выводы:")
    print("  1. try/except — перехват и обработка исключений")
    print("  2. else — код, если исключений не было; finally — код в любом случае")
    print("  3. raise — возбуждение исключения; raise from — цепочка")
    print("  4. Свои исключения: наследуйтесь от Exception")
    print("  5. with (контекстный менеджер) — автоматическое освобождение ресурсов")
    print("=" * 50)


if __name__ == "__main__":
    main()
