"""
Урок 23: JSON и CSV в Python
=============================

Темы:
  - JSON: dump/load (файлы), dumps/loads (строки)
  - Кастомная сериализация (default, object_hook)
  - CSV: reader/writer, DictReader/DictWriter
  - Диалекты CSV, кастомные разделители
  - Практические примеры
"""

import json
import csv
import io
from datetime import datetime
from pathlib import Path


# =============================================================================
# 1. JSON — СЕРИАЛИЗАЦИЯ
# =============================================================================

def json_serialization_demo():
    """Запись Python-объектов в JSON."""
    print("=" * 60)
    print("1. JSON — СЕРИАЛИЗАЦИЯ (Python → JSON)")
    print("=" * 60)

    data = {
        "users": [
            {"id": 1, "name": "Анна", "active": True, "score": 95.5, "tags": ["python", "js"]},
            {"id": 2, "name": "Борис", "active": False, "score": 88.0, "tags": None},
        ],
        "total": 2,
        "version": "1.0",
        "metadata": None,
    }

    # json.dumps() — объект → строка
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print("json.dumps (строка):")
    print(json_str[:200])

    # json.dump() — объект → файл
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("\n[OK] data.json записан")

    # Параметры
    compact = json.dumps(data, ensure_ascii=False)           # Без отступов
    sorted_keys = json.dumps(data, ensure_ascii=False,       # Ключи по алфавиту
                             sort_keys=True, indent=2)
    print(f"\nCompact: {len(compact)} символов")
    print(f"Pretty:  {len(json_str)} символов")


# =============================================================================
# 2. JSON — ДЕСЕРИАЛИЗАЦИЯ
# =============================================================================

def json_deserialization_demo():
    """Чтение JSON в Python-объекты."""
    print("\n" + "=" * 60)
    print("2. JSON — ДЕСЕРИАЛИЗАЦИЯ (JSON → Python)")
    print("=" * 60)

    # json.loads() — строка → объект
    json_str = '{"name": "Анна", "age": 28, "skills": ["Python", "QA"]}'
    obj = json.loads(json_str)
    print(f"json.loads: {obj}")
    print(f"  name={obj['name']}, type={type(obj)}")

    # json.load() — файл → объект
    with open("data.json", "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"\nИз файла: total={loaded['total']}, users={len(loaded['users'])}")

    # Очистка
    Path("data.json").unlink()


# =============================================================================
# 3. КАСТОМНАЯ СЕРИАЛИЗАЦИЯ JSON
# =============================================================================

def custom_serializer(obj):
    """Обработчик нестандартных типов."""
    if isinstance(obj, datetime):
        return {"__type__": "datetime", "value": obj.isoformat()}
    if isinstance(obj, set):
        return list(obj)
    if hasattr(obj, "__dict__"):
        return {"__type__": type(obj).__name__, "value": obj.__dict__}
    raise TypeError(f"Type {type(obj)} not serializable")


def custom_json_demo():
    """Демонстрация кастомной сериализации."""
    print("\n" + "=" * 60)
    print("3. КАСТОМНАЯ JSON СЕРИАЛИЗАЦИЯ")
    print("=" * 60)

    complex_data = {
        "created_at": datetime.now(),
        "tags": {"python", "testing"},
    }

    # default — функция для нестандартных типов
    json_str = json.dumps(complex_data, default=custom_serializer,
                          ensure_ascii=False, indent=2)
    print(f"С complex типами:\n{json_str}")

    # object_hook — восстанавливает объекты при чтении
    def object_hook(dct):
        if "__type__" in dct:
            if dct["__type__"] == "datetime":
                return datetime.fromisoformat(dct["value"])
        return dct

    restored = json.loads(json_str, object_hook=object_hook)
    print(f"Восстановлен: created_at = {restored['created_at']} "
          f"({type(restored['created_at']).__name__})")


# =============================================================================
# 4. CSV — ЗАПИСЬ И ЧТЕНИЕ
# =============================================================================

def csv_demo():
    """Демонстрация CSV."""
    print("\n" + "=" * 60)
    print("4. CSV")
    print("=" * 60)

    users = [
        {"name": "Анна", "age": 28, "city": "Москва"},
        {"name": "Борис", "age": 35, "city": "Питер"},
        {"name": "Вера", "age": 22, "city": "Казань"},
    ]

    # --- DictWriter (запись словарей) ---
    with open("users.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["name", "age", "city"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)
    print("[OK] users.csv записан")

    # --- DictReader (чтение как словари) ---
    with open("users.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("Содержимое:")
        for row in reader:
            print(f"  {row['name']}, {row['age']} лет, г. {row['city']}")

    # --- Обычный reader/writer ---
    with open("matrix.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([[i * j for j in range(1, 6)] for i in range(1, 6)])
    print("[OK] matrix.csv записан")

    # Кастомный разделитель
    with open("semicolon.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["колонка1", "колонка2"])
        writer.writerow(["знач1", "знач2"])

    # Очистка
    for f in ["users.csv", "matrix.csv", "semicolon.csv"]:
        Path(f).unlink()


# =============================================================================
# 5. ПРАКТИЧЕСКИЙ ПРИМЕР
# =============================================================================

def practical_example():
    """Практический пример: конвертация JSON ↔ CSV."""
    print("\n" + "=" * 60)
    print("5. ПРАКТИЧЕСКИЙ ПРИМЕР: JSON ↔ CSV")
    print("=" * 60)

    # JSON → CSV
    json_data = [
        {"product": "Ноутбук", "price": 50000, "stock": 10},
        {"product": "Мышь", "price": 2000, "stock": 50},
        {"product": "Клавиатура", "price": 3500, "stock": 30},
    ]

    # Запись JSON
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # JSON → CSV конвертация
    with open("products.json", "r", encoding="utf-8") as fj, \
         open("products.csv", "w", newline="", encoding="utf-8") as fc:
        data = json.load(fj)
        writer = csv.DictWriter(fc, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print("[OK] products.json → products.csv")

    # Читаем CSV и считаем общую стоимость
    with open("products.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        total_value = sum(int(row["price"]) * int(row["stock"]) for row in reader)
    print(f"Общая стоимость товаров: {total_value:,} ₽".replace(",", " "))

    # Очистка
    Path("products.json").unlink()
    Path("products.csv").unlink()


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    json_serialization_demo()
    json_deserialization_demo()
    custom_json_demo()
    csv_demo()
    practical_example()

    print("\n" + "=" * 60)
    print("✅ УРОК 23 ЗАВЕРШЁН: JSON И CSV ОСВОЕНЫ!")
    print("=" * 60)
