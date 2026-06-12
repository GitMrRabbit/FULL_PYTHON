# 📝 Урок 29: Логирование

## 📖 Уровни логирования (от низшего к высшему)

| Уровень | Когда использовать |
|---------|-------------------|
| DEBUG | Детальная отладка |
| INFO | Ключевые события |
| WARNING | Потенциальная проблема |
| ERROR | Ошибка, требует внимания |
| CRITICAL | Критический сбой |

---

## 🔹 Базовая настройка

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Приложение запущено")
```

---

## 🔹 Расширенная настройка

```python
# Файловый handler с ротацией
file_handler = logging.handlers.RotatingFileHandler(
    "app.log", maxBytes=1_000_000, backupCount=3
)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logger = logging.getLogger("myapp")
logger.addHandler(file_handler)
```

---

## 🔹 Структурное логирование (JSON)

```python
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        })

handler.setFormatter(JsonFormatter())
```

---

## 💡 Лучшие практики

1. `logger = logging.getLogger(__name__)` — не root logger
2. **Не логируйте пароли/токены**
3. **Используйте ротацию файлов**
4. **Структурные логи (JSON)** для production
5. **`logger.exception()`** в except-блоке (автоматический трейсбек)

## 🧪 Упражнения

1. Настройте логирование в файл с ротацией
2. Создайте декоратор `@log_execution` для функций
3. Реализуйте JSON-форматтер для логов
4. Добавьте request_id в контекст логирования
