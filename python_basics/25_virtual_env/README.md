# 📦 Урок 25: Виртуальные окружения и зависимости

## 📖 Зачем?

Виртуальное окружение (venv) — изолированная среда Python для проекта. Позволяет каждому проекту иметь свои версии библиотек без конфликтов.

---

## 🔹 Создание и активация

```bash
# Создание
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/Mac)
source venv/bin/activate

# Деактивация
deactivate
```

---

## 🔹 pip — менеджер пакетов

```bash
pip install requests              # Установить
pip install requests==2.28.0      # Конкретная версия
pip install -r requirements.txt   # Из файла
pip freeze > requirements.txt     # Сохранить все версии
pip list                          # Список установленных
pip uninstall requests            # Удалить
```

---

## 🔹 requirements.txt

```
requests>=2.28.0,<3.0.0
pydantic~=2.0.0     # ~= совместимая (2.0.x)
pytest==7.4.0       # Точная версия
```

---

## 🔹 Структура проекта

```
my_project/
├── venv/                # В .gitignore!
├── src/                 # Исходный код
├── tests/               # Тесты
├── requirements.txt     # Зависимости
├── README.md
└── .gitignore
```

---

## 💡 Лучшие практики

1. **Всегда venv** — для каждого проекта
2. **venv/ в .gitignore** — не коммитить окружение
3. **requirements.txt коммитить** — фиксировать зависимости
4. **Разделять prod/dev зависимости**
5. **pip-tools или Poetry** для сложных проектов

## 🧪 Упражнения

1. Создайте виртуальное окружение и установите requests
2. Создайте requirements.txt для существующего проекта
3. Настройте .gitignore для Python-проекта
