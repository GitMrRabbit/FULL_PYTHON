# 📁 Урок 14: Работа с файлами в Python

## 📖 Теория

### Зачем нужна работа с файлами?

Файлы — основной способ долговременного хранения данных. Практически любая программа читает или записывает файлы: конфигурации, логи, отчёты, базы данных, изображения, JSON-ответы от API.

---

## 🔧 Режимы открытия файлов

| Режим | Описание | Создаёт файл? | Перезаписывает? |
|-------|----------|:---:|:---:|
| `'r'` | Только чтение | ❌ | ❌ |
| `'w'` | Запись (перезапись) | ✅ | ✅ |
| `'a'` | Дозапись в конец | ✅ | ❌ |
| `'x'` | Эксклюзивное создание | ✅ | ❌ (ошибка если есть) |
| `'r+'`| Чтение + запись | ❌ | ❌ |
| `'w+'`| Запись + чтение | ✅ | ✅ |
| `'a+'`| Дозапись + чтение | ✅ | ❌ |
| `'rb'`| Бинарное чтение | ❌ | ❌ |
| `'wb'`| Бинарная запись | ✅ | ✅ |

---

## 📝 Основные методы

### Чтение:
```python
f.read()        # Весь файл как строка
f.readline()    # Одна строка
f.readlines()   # Список всех строк
for line in f:  # Построчная итерация (экономит память!)
    ...
```

### Запись:
```python
f.write("текст")         # Запись строки
f.writelines(["a\n", "b\n"])  # Запись списка строк
```

---

## 🎯 `with` — контекстный менеджер

**Всегда используйте `with`!** Он гарантирует закрытие файла даже при ошибке:

```python
# ✅ ПРАВИЛЬНО
with open("file.txt", "r", encoding="utf-8") as f:
    data = f.read()
# Файл автоматически закрыт

# ❌ НЕПРАВИЛЬНО (можно забыть close())
f = open("file.txt", "r")
data = f.read()
f.close()  # А если исключение до этой строки?
```

---

## 🛤️ `pathlib.Path` — современная работа с путями

Начиная с Python 3.4, `pathlib` — рекомендуемый способ:

```python
from pathlib import Path

# Создание пути
p = Path("data") / "users" / "profile.json"

# Методы
p.exists()        # Существует ли?
p.is_file()       # Это файл?
p.is_dir()        # Это директория?
p.name            # "profile.json"
p.suffix          # ".json"
p.stem            # "profile"
p.parent          # Path("data/users")
p.read_text()     # Прочитать как текст
p.write_text("...")  # Записать текст

# Создание директорий
Path("deep/nested/dir").mkdir(parents=True, exist_ok=True)

# Поиск файлов
for py_file in Path(".").glob("*.py"):    # Все .py в текущей
    print(py_file)

for txt_file in Path(".").rglob("*.txt"):  # Рекурсивно все .txt
    print(txt_file)
```

---

## 📊 CSV (Comma-Separated Values)

```python
import csv

# Чтение как словарь
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])

# Запись как словарь
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows([{"name": "Анна", "age": 28}])
```

---

## 🌐 JSON (JavaScript Object Notation)

```python
import json

# Python → JSON (сериализация)
data = {"users": [{"name": "Анна"}]}
json.dump(data, f, ensure_ascii=False, indent=2)   # В файл
json.dumps(data, ensure_ascii=False)                # В строку

# JSON → Python (десериализация)
data = json.load(f)          # Из файла
data = json.loads('{"key": "value"}')  # Из строки
```

---

## ⚠️ Типичные ошибки

| Ошибка | Причина |
|--------|---------|
| `FileNotFoundError` | Файл не существует (режим 'r') |
| `PermissionError` | Нет прав на чтение/запись |
| `IsADirectoryError` | Пытаемся открыть директорию как файл |
| `UnicodeDecodeError` | Неправильная кодировка (используйте `encoding="utf-8"`) |
| `FileExistsError` | Режим 'x', а файл уже есть |

---

## 💡 Лучшие практики

1. **Всегда `with`** — никогда не открывайте файлы без контекстного менеджера
2. **Всегда `encoding="utf-8"`** — явно указывайте кодировку
3. **`pathlib` > `os.path`** — используйте современный Path API
4. **Построчное чтение** для больших файлов — `for line in f:`
5. **Не читайте всё в память** для больших бинарных файлов — используйте `f.read(chunk_size)`

---

## 🧪 Упражнения

1. Напишите скрипт, который читает CSV-файл и выводит средний возраст по городам
2. Создайте функцию `backup_files(extension)`, копирующую все файлы с заданным расширением в папку `backup/`
3. Реализуйте класс `JsonDatabase` для хранения записей в JSON-файле с методами `insert()`, `select()`, `update()`, `delete()`
4. Напишите логгер, который дописывает сообщения с временной меткой в файл
