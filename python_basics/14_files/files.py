"""
Урок 14: Работа с файлами в Python
====================================

Темы:
  - Открытие/закрытие файлов: open(), режимы (r, w, a, x, rb, wb)
  - Чтение: read(), readline(), readlines()
  - Запись: write(), writelines()
  - Контекстный менеджер with
  - pathlib.Path — современный способ работы с путями
  - Работа с CSV (модуль csv)
  - Работа с JSON (модуль json)
  - Обработка ошибок при работе с файлами
  - Временные файлы (модуль tempfile)
"""

import os
import csv
import json
import tempfile
from pathlib import Path

# =============================================================================
# 1. БАЗОВЫЕ ОПЕРАЦИИ С ФАЙЛАМИ
# =============================================================================

def basic_file_operations():
    """Демонстрация базовых операций: запись и чтение текстовых файлов."""
    print("=" * 60)
    print("1. БАЗОВЫЕ ОПЕРАЦИИ С ФАЙЛАМИ")
    print("=" * 60)

    # --- Запись в файл (режим 'w' — перезапись) ---
    # Если файл существует, он будет ПЕРЕЗАПИСАН
    with open("example.txt", "w", encoding="utf-8") as f:
        f.write("Первая строка\n")
        f.write("Вторая строка\n")
        f.write("Третья строка\n")
    print("[OK] Файл example.txt записан (режим 'w')")

    # --- Чтение всего файла целиком ---
    with open("example.txt", "r", encoding="utf-8") as f:
        content = f.read()          # Читает ВЕСЬ файл в одну строку
    print(f"\nread() — весь файл:\n{content}")

    # --- Чтение построчно ---
    with open("example.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()       # Возвращает список строк
    print(f"readlines() — список строк: {lines}")

    # --- Построчное чтение (экономит память для больших файлов) ---
    with open("example.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            print(f"  Строка {i}: {line.rstrip()}")

    # Удаляем тестовый файл
    os.remove("example.txt")


# =============================================================================
# 2. РЕЖИМЫ ОТКРЫТИЯ ФАЙЛОВ
# =============================================================================

def file_modes_demo():
    """Демонстрация всех режимов открытия файлов."""
    print("\n" + "=" * 60)
    print("2. РЕЖИМЫ ОТКРЫТИЯ ФАЙЛОВ")
    print("=" * 60)

    filename = "modes_demo.txt"

    # 'w' — write (перезапись). Создаёт файл, если его нет
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Строка 1\n")

    # 'a' — append (дозапись в конец). Не удаляет содержимое
    with open(filename, "a", encoding="utf-8") as f:
        f.write("Строка 2 (добавлена)\n")

    # 'r' — read (только чтение). Ошибка, если файла нет
    with open(filename, "r", encoding="utf-8") as f:
        print(f"Содержимое после 'a': {f.read().rstrip()}")

    # 'x' — exclusive creation. Ошибка, если файл уже существует
    try:
        with open("new_exclusive.txt", "x", encoding="utf-8") as f:
            f.write("Эксклюзивно созданный файл\n")
        print("[OK] Файл создан в режиме 'x'")
        os.remove("new_exclusive.txt")
    except FileExistsError:
        print("[!] Файл уже существует (режим 'x')")

    # 'r+' — чтение и запись (файл должен существовать)
    with open(filename, "r+", encoding="utf-8") as f:
        content = f.read()
        f.write("Строка 3 (через r+)\n")

    # 'w+' — запись и чтение (перезаписывает файл)
    # 'a+' — дозапись и чтение

    os.remove(filename)
    print("[OK] Все режимы продемонстрированы")


# =============================================================================
# 3. КОНТЕКСТНЫЙ МЕНЕДЖЕР with
# =============================================================================

def context_manager_demo():
    """
    Демонстрация контекстного менеджера with.
    
    with гарантирует закрытие файла, даже если произошла ошибка.
    Это эквивалентно try/finally, но короче и безопаснее.
    """
    print("\n" + "=" * 60)
    print("3. КОНТЕКСТНЫЙ МЕНЕДЖЕР with")
    print("=" * 60)

    # ПЛОХО: без with — файл может не закрыться при ошибке
    # f = open("test.txt", "w")
    # f.write("данные")
    # f.close()  # Что если write() выбросит исключение?

    # ХОРОШО: with гарантирует закрытие
    with open("test_with.txt", "w", encoding="utf-8") as f:
        f.write("Данные записаны через with\n")
        # Даже если здесь будет исключение, файл закроется!

    # Можно открывать несколько файлов одновременно (через запятую)
    with (
        open("file1.txt", "w", encoding="utf-8") as f1,
        open("file2.txt", "w", encoding="utf-8") as f2,
    ):
        f1.write("Файл 1\n")
        f2.write("Файл 2\n")

    print("[OK] Контекстный менеджер продемонстрирован")
    os.remove("test_with.txt")
    os.remove("file1.txt")
    os.remove("file2.txt")


# =============================================================================
# 4. PATHLIB — СОВРЕМЕННАЯ РАБОТА С ПУТЯМИ
# =============================================================================

def pathlib_demo():
    """
    Демонстрация pathlib.Path — современного и удобного способа
    работы с файловыми путями (Python 3.4+).
    
    Преимущества перед os.path:
      - Объектно-ориентированный подход
      - Оператор / для склеивания путей
      - Единый API для всех ОС (Windows/Linux/Mac)
    """
    print("\n" + "=" * 60)
    print("4. PATHLIB — СОВРЕМЕННАЯ РАБОТА С ПУТЯМИ")
    print("=" * 60)

    # Создание путей
    home = Path.home()                      # Домашняя директория
    current = Path.cwd()                    # Текущая рабочая директория
    print(f"Домашняя директория: {home}")
    print(f"Текущая директория:  {current}")

    # Склеивание путей через / (очень удобно!)
    data_dir = Path(".") / "data" / "subdir"
    print(f"Склеенный путь: {data_dir}")

    # Создание директории (включая родительские)
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Директория создана: {data_dir}")

    # Создание файла
    file_path = data_dir / "example.txt"
    file_path.write_text("Привет из pathlib!", encoding="utf-8")
    print(f"[OK] Файл создан: {file_path}")

    # Чтение файла
    content = file_path.read_text(encoding="utf-8")
    print(f"Содержимое: {content}")

    # Информация о файле
    print(f"  Имя файла:      {file_path.name}")
    print(f"  Расширение:      {file_path.suffix}")
    print(f"  Без расширения:  {file_path.stem}")
    print(f"  Родитель:        {file_path.parent}")
    print(f"  Существует:      {file_path.exists()}")
    print(f"  Это файл:        {file_path.is_file()}")
    print(f"  Это директория:  {file_path.is_dir()}")
    print(f"  Размер:          {file_path.stat().st_size} байт")

    # Итерация по директории
    print(f"\nСодержимое {data_dir}:")
    for item in data_dir.iterdir():
        print(f"  - {item.name}")

    # Поиск файлов по шаблону (glob)
    py_files = list(Path(".").glob("*.py"))
    print(f"\nPython-файлы в текущей директории: {len(py_files)} шт.")

    # Рекурсивный поиск
    all_txt = list(Path(".").rglob("*.txt"))
    print(f"Все .txt файлы (рекурсивно): {len(all_txt)} шт.")

    # Очистка
    file_path.unlink()          # Удалить файл
    data_dir.rmdir()            # Удалить пустую директорию
    print("[OK] Очистка завершена")


# =============================================================================
# 5. РАБОТА С CSV
# =============================================================================

def csv_demo():
    """
    Демонстрация работы с CSV-файлами.
    
    CSV (Comma-Separated Values) — текстовый формат для табличных данных.
    """
    print("\n" + "=" * 60)
    print("5. РАБОТА С CSV")
    print("=" * 60)

    csv_file = "users.csv"

    # --- Запись CSV (список словарей) ---
    users = [
        {"name": "Анна",  "age": 28, "city": "Москва"},
        {"name": "Борис", "age": 35, "city": "Питер"},
        {"name": "Вера",  "age": 22, "city": "Казань"},
    ]

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["name", "age", "city"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()        # Заголовки колонок
        writer.writerows(users)     # Все строки разом
        # writer.writerow(row)      # По одной строке

    print(f"[OK] CSV записан: {csv_file}")

    # --- Чтение CSV как список словарей ---
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("Содержимое CSV:")
        for row in reader:
            print(f"  {row['name']}, {row['age']} лет, г. {row['city']}")
            # Значения всегда строки! Нужно приводить типы:
            age = int(row["age"])

    # --- Чтение CSV как список списков ---
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)       # Пропускаем заголовок
        print(f"\nЗаголовки: {header}")
        for row in reader:
            print(f"  Строка: {row}")

    # --- Пользовательский диалект (разделитель ; вместо ,) ---
    csv.register_dialect("my_dialect", delimiter=";", quoting=csv.QUOTE_MINIMAL)
    with open("custom.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, dialect="my_dialect")
        writer.writerow(["колонка1", "колонка2"])
        writer.writerow(["значение1", "значение2"])

    os.remove(csv_file)
    os.remove("custom.csv")
    print("[OK] CSV демонстрация завершена")


# =============================================================================
# 6. РАБОТА С JSON
# =============================================================================

def json_demo():
    """
    Демонстрация работы с JSON.
    
    JSON (JavaScript Object Notation) — основной формат обмена данными в вебе.
    """
    print("\n" + "=" * 60)
    print("6. РАБОТА С JSON")
    print("=" * 60)

    json_file = "data.json"

    # --- Python → JSON (сериализация) ---
    data = {
        "users": [
            {"id": 1, "name": "Анна",  "active": True,  "score": 95.5, "tags": ["python", "js"]},
            {"id": 2, "name": "Борис", "active": False, "score": 88.0, "tags": ["java"]},
        ],
        "total": 2,
        "version": "1.0"
    }

    # json.dump() — запись в файл
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] JSON записан в {json_file}")

    # json.dumps() — в строку (для API-запросов, логов и т.д.)
    json_string = json.dumps(data, ensure_ascii=False, indent=2)
    print(f"JSON строка (первые 80 символов): {json_string[:80]}...")

    # --- JSON → Python (десериализация) ---
    with open(json_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)       # json.load() — из файла
    print(f"\nЗагружено из файла: {loaded['users'][0]['name']}")

    # json.loads() — из строки
    parsed = json.loads('{"key": "value", "num": 42}')
    print(f"Парсинг строки: {parsed}")

    # --- Кастомный сериализатор для нестандартных типов ---
    from datetime import datetime

    def custom_serializer(obj):
        """Сериализатор для объектов, которые json не умеет по умолчанию."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Тип {type(obj)} не сериализуется")

    complex_data = {
        "created_at": datetime.now(),
        "unique_tags": {"python", "testing", "automation"}
    }
    json_str = json.dumps(complex_data, default=custom_serializer, ensure_ascii=False, indent=2)
    print(f"\nСложный объект в JSON:\n{json_str}")

    os.remove(json_file)
    print("[OK] JSON демонстрация завершена")


# =============================================================================
# 7. БИНАРНЫЕ ФАЙЛЫ
# =============================================================================

def binary_files_demo():
    """Демонстрация работы с бинарными файлами (изображения, архивы и т.д.)."""
    print("\n" + "=" * 60)
    print("7. БИНАРНЫЕ ФАЙЛЫ")
    print("=" * 60)

    # Запись бинарных данных
    binary_data = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F])  # "Hello" в байтах

    with open("binary.dat", "wb") as f:     # 'wb' — write binary
        f.write(binary_data)
    print(f"[OK] Бинарный файл записан: {binary_data}")

    # Чтение бинарных данных
    with open("binary.dat", "rb") as f:     # 'rb' — read binary
        read_data = f.read()
    print(f"Прочитано: {read_data} → '{read_data.decode('utf-8')}'")

    # Копирование файла блоками (экономия памяти для больших файлов)
    chunk_size = 1024  # 1 КБ
    with open("binary.dat", "rb") as src, open("binary_copy.dat", "wb") as dst:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            dst.write(chunk)
    print("[OK] Файл скопирован блоками")

    os.remove("binary.dat")
    os.remove("binary_copy.dat")


# =============================================================================
# 8. ВРЕМЕННЫЕ ФАЙЛЫ
# =============================================================================

def tempfile_demo():
    """Демонстрация работы с временными файлами через модуль tempfile."""
    print("\n" + "=" * 60)
    print("8. ВРЕМЕННЫЕ ФАЙЛЫ (tempfile)")
    print("=" * 60)

    # Временный файл (автоматически удаляется при закрытии)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=True, encoding="utf-8") as tmp:
        tmp.write("Временные данные\n")
        tmp.flush()                     # Принудительно сбрасываем буфер
        print(f"Временный файл: {tmp.name}")
        print(f"Существует: {os.path.exists(tmp.name)}")
    print(f"После закрытия существует: {os.path.exists(tmp.name)}")

    # Временная директория
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / "temp_file.txt"
        tmp_path.write_text("Данные во временной директории", encoding="utf-8")
        print(f"\nВременная директория: {tmp_dir}")
        print(f"Файл внутри: {tmp_path}")
        print(f"Существует: {tmp_path.exists()}")
    print(f"После выхода из with: {os.path.exists(tmp_dir)}")

    print("[OK] Временные файлы продемонстрированы")


# =============================================================================
# 9. ОБРАБОТКА ОШИБОК ПРИ РАБОТЕ С ФАЙЛАМИ
# =============================================================================

def file_error_handling():
    """Демонстрация правильной обработки ошибок при работе с файлами."""
    print("\n" + "=" * 60)
    print("9. ОБРАБОТКА ОШИБОК")
    print("=" * 60)

    # FileNotFoundError — файл не найден
    try:
        with open("несуществующий_файл.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("[OK] Перехвачен FileNotFoundError — файла нет")

    # PermissionError — нет прав на чтение/запись
    try:
        with open("/root/secret.txt", "r") as f:  # На Windows будет PermissionError
            pass
    except (PermissionError, FileNotFoundError):
        print("[OK] Перехвачен PermissionError / FileNotFoundError")

    # IsADirectoryError — пытаемся открыть директорию как файл
    try:
        with open(".", "r") as f:
            pass
    except IsADirectoryError:
        print("[OK] Перехвачен IsADirectoryError — это директория")

    # Безопасное чтение с проверкой существования
    target = Path("maybe_exists.txt")
    if target.exists():
        content = target.read_text(encoding="utf-8")
    else:
        print(f"[INFO] Файл {target} не существует — пропускаем")

    print("[OK] Обработка ошибок продемонстрирована")


# =============================================================================
# 10. ПРАКТИЧЕСКИЙ ПРИМЕР: КОНФИГ-МЕНЕДЖЕР
# =============================================================================

class FileConfigManager:
    """
    Практический пример: простой менеджер конфигурации в JSON.
    Демонстрирует паттерн «загрузить — изменить — сохранить».
    """

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self._config: dict = {}

    def load(self) -> dict:
        """Загружает конфигурацию из файла."""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
        else:
            self._config = {}
        return self._config

    def get(self, key: str, default=None):
        """Получить значение по ключу."""
        return self._config.get(key, default)

    def set(self, key: str, value):
        """Установить значение."""
        self._config[key] = value

    def save(self):
        """Сохранить конфигурацию в файл."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, *args):
        self.save()


def practical_example():
    """Демонстрация практического использования FileConfigManager."""
    print("\n" + "=" * 60)
    print("10. ПРАКТИЧЕСКИЙ ПРИМЕР: КОНФИГ-МЕНЕДЖЕР")
    print("=" * 60)

    config_path = Path("app_config.json")

    # Использование с контекстным менеджером
    with FileConfigManager(config_path) as cfg:
        cfg.set("app_name", "MyPythonApp")
        cfg.set("version", "1.0.0")
        cfg.set("debug", True)
        print(f"Конфиг в памяти: {cfg.load()}")

    # Проверяем, что файл создался
    print(f"Файл создан: {config_path.exists()}")
    print(f"Содержимое файла:\n{config_path.read_text()}")

    # Читаем обратно
    with FileConfigManager(config_path) as cfg:
        print(f"app_name = {cfg.get('app_name')}")
        print(f"version  = {cfg.get('version')}")
        print(f"debug    = {cfg.get('debug')}")

    # Очистка
    config_path.unlink()
    print("[OK] Практический пример завершён")


# =============================================================================
# ЗАПУСК ВСЕХ ДЕМОНСТРАЦИЙ
# =============================================================================

if __name__ == "__main__":
    basic_file_operations()
    file_modes_demo()
    context_manager_demo()
    pathlib_demo()
    csv_demo()
    json_demo()
    binary_files_demo()
    tempfile_demo()
    file_error_handling()
    practical_example()

    print("\n" + "=" * 60)
    print("✅ УРОК 14 ЗАВЕРШЁН: ФАЙЛЫ ОСВОЕНЫ!")
    print("=" * 60)
