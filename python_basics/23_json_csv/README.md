# 📊 Урок 23: JSON и CSV

## JSON (JavaScript Object Notation)

```python
import json

# Python → JSON
json.dumps(obj, ensure_ascii=False, indent=2)         # в строку
json.dump(obj, file, ensure_ascii=False, indent=2)     # в файл

# JSON → Python
obj = json.loads(json_string)   # из строки
obj = json.load(file)           # из файла
```

### Кастомная сериализация
```python
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError

json.dumps(data, default=custom_serializer)
```

### Соответствие типов

| Python | JSON |
|--------|------|
| dict | object |
| list, tuple | array |
| str | string |
| int, float | number |
| True/False | true/false |
| None | null |

## CSV

```python
import csv

# Чтение словарей
with open("file.csv") as f:
    for row in csv.DictReader(f):
        print(row["column_name"])

# Запись словарей
with open("file.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["col1", "col2"])
    writer.writeheader()
    writer.writerows(data)
```

## 🧪 Упражнения
1. Конвертируйте JSON-файл в CSV и обратно
2. Сериализуйте объект Python с datetime в JSON через кастомный default
3. Прочитайте CSV с разделителем `;` и сохраните как JSON
