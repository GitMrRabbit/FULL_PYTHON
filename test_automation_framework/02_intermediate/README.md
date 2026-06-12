# 🧪 Test Automation Framework — Уровень 2: Intermediate

## Page Object Model + DTO + Фабрики

Этот уровень демонстрирует паттерны автоматизации тестирования:
- **Page Object Model** — страницы как объекты
- **DTO (Data Transfer Objects)** — модели данных
- **Factory** — фабрики тестовых данных
- **Configuration** — YAML-конфигурация

---

## Структура

```
02_intermediate/
├── config/           # Конфигурация (YAML)
├── pages/            # Page Objects (SauceDemo)
├── components/       # UI-компоненты (header, footer)
├── dto/              # Data Transfer Objects
├── factories/        # Фабрики тестовых данных
├── tests/            # Тесты (login, inventory, cart, checkout)
├── utils/            # Утилиты (driver_factory, wait_helpers)
├── data/             # Тестовые данные (JSON)
├── conftest.py       # Фикстуры
└── pytest.ini        # Настройки pytest
```

---

## Запуск

```bash
pip install pytest selenium pyyaml
pytest test_automation_framework/02_intermediate/ -v
```

## Ключевые концепции

1. **BasePage** — базовые методы (find, click, wait)
2. **Наследование страниц** — LoginPage, InventoryPage, CartPage
3. **DTO и dataclass** — UserDTO, ProductDTO, OrderDTO
4. **Фабрики** — генерация тестовых данных
5. **Скриншоты при падении** — фикстура в conftest
