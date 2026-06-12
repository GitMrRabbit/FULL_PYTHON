"""
test_fixtures.py — Фикстуры: setup/teardown, scope, yield

Показывает:
- Как работают фикстуры (аналог setUp/tearDown)
- scope: function, class, module, session
- yield — teardown после выполнения теста
- Фикстуры, зависящие от других фикстур
- autouse фикстуры
- conftest.py фикстуры
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
from calculator import Calculator


# ============================================================
# ФИКСТУРЫ С YIELD (setup + teardown)
# ============================================================

@pytest.fixture
def db_connection():
    """
    Фикстура с yield — эмулирует подключение к БД.
    
    Код ДО yield — setup (подготовка).
    Код ПОСЛЕ yield — teardown (очистка).
    """
    print("\n  [Фикстура] 🔌 Подключаюсь к БД...")
    # Setup: создаём "подключение"
    connection = {"status": "connected", "db": "test_db"}
    
    # yield — передача объекта в тест
    yield connection
    
    # Teardown: выполняется после теста
    print("\n  [Фикстура] 🔌 Закрываю подключение к БД...")
    connection["status"] = "disconnected"


def test_with_db(db_connection):
    """Тест использует фикстуру с setup/teardown."""
    print("  [Тест] Работаю с БД...")
    assert db_connection["status"] == "connected"
    assert db_connection["db"] == "test_db"


def test_db_closed_after_test():
    """
    После теста фикстура отработала teardown.
    Но каждый тест получает СВОЙ экземпляр фикстуры,
    так что здесь connection снова "connected".
    """
    # Этот тест демонстрирует, что фикстуры изолированы
    pass


# ============================================================
# SCOPE (ОБЛАСТЬ ДЕЙСТВИЯ ФИКСТУР)
# ============================================================

# scope='function' (по умолчанию) — новая фикстура для КАЖДОГО теста
# scope='class' — одна на класс
# scope='module' — одна на модуль (файл)
# scope='session' — одна на всю сессию тестов

call_count_function = 0

@pytest.fixture(scope="function")
def function_scoped():
    """Создаётся заново для каждого теста."""
    global call_count_function
    call_count_function += 1
    return f"function_call_{call_count_function}"


def test_function_scope_1(function_scoped):
    print(f"  test_1: {function_scoped}")

def test_function_scope_2(function_scoped):
    print(f"  test_2: {function_scoped}")


call_count_module = 0

@pytest.fixture(scope="module")
def module_scoped():
    """Создаётся ОДИН раз на весь модуль."""
    global call_count_module
    call_count_module += 1
    print(f"\n  [module_scoped] Создаю (вызов #{call_count_module})")
    return f"module_call_{call_count_module}"


def test_module_scope_1(module_scoped):
    print(f"  test_1: {module_scoped}")

def test_module_scope_2(module_scoped):
    print(f"  test_2: {module_scoped} (то же значение!)")


# ============================================================
# ЦЕПОЧКИ ФИКСТУР (одна зависит от другой)
# ============================================================

@pytest.fixture
def base_data():
    """Базовая фикстура с данными."""
    return {"name": "Анна", "age": 25}


@pytest.fixture
def enriched_data(base_data):
    """Фикстура, зависящая от base_data — добавляет поля."""
    data = base_data.copy()
    data["city"] = "Москва"
    data["email"] = "anna@example.com"
    return data


def test_fixture_chaining(enriched_data):
    """Тест использует фикстуру, которая использует другую фикстуру."""
    assert enriched_data["name"] == "Анна"
    assert enriched_data["age"] == 25
    assert enriched_data["city"] == "Москва"
    assert enriched_data["email"] == "anna@example.com"


# ============================================================
# AUTOUSE — автоматически применяемая фикстура
# ============================================================

@pytest.fixture(autouse=True)
def auto_reset():
    """
    autouse=True — фикстура применяется ко ВСЕМ тестам автоматически.
    Полезно для: логирования, очистки кэша, настройки окружения.
    
    Внимание: может замедлить тесты!
    """
    print("\n  [autouse] Подготовка окружения...")
    yield
    print("\n  [autouse] Очистка окружения...")


# ============================================================
# ПАРАМЕТРИЗОВАННЫЕ ФИКСТУРЫ
# ============================================================

@pytest.fixture(params=[10, 100, 1000])
def multiplier(request):
    """
    Фикстура с params: тест будет вызван для КАЖДОГО параметра.
    request.param содержит текущее значение.
    """
    return request.param


def test_with_multiplier(calculator, multiplier):
    """Тест запускается 3 раза с multiplier = 10, 100, 1000."""
    calculator.add(multiplier)
    assert calculator.value == multiplier


# ============================================================
# ВРЕМЕННЫЕ ФАЙЛЫ И ДИРЕКТОРИИ
# ============================================================

@pytest.fixture
def temp_file(tmp_path):
    """
    tmp_path — встроенная фикстура pytest.
    Создаёт временную директорию, уникальную для каждого теста.
    """
    file = tmp_path / "test_data.txt"
    file.write_text("Hello, pytest!")
    return file


def test_temp_file(temp_file):
    """Чтение из временного файла."""
    assert temp_file.exists()
    content = temp_file.read_text()
    assert content == "Hello, pytest!"


def test_temp_file_isolated(tmp_path):
    """Каждый тест имеет СВОЮ временную директорию."""
    file = tmp_path / "my_file.txt"
    file.write_text("test")
    assert file.read_text() == "test"
    # После теста директория будет удалена автоматически
