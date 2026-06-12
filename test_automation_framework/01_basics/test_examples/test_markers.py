"""
test_markers.py — Маркеры: skip, skipif, xfail, кастомные маркеры

Показывает:
- @pytest.mark.skip — пропустить тест
- @pytest.mark.skipif — пропустить по условию
- @pytest.mark.xfail — ожидаемое падение
- Кастомные маркеры для группировки тестов
- Запуск по маркерам: pytest -m "smoke"
"""

import pytest
import sys


# ============================================================
# SKIP — ПРОПУСТИТЬ ТЕСТ
# ============================================================

@pytest.mark.skip(reason="Этот тест пока не реализован")
def test_not_ready():
    """Тест будет ПРОПУЩЕН с указанием причины."""
    assert False  # Никогда не выполнится


def test_will_run():
    """Обычный тест — выполняется."""
    assert True


# ============================================================
# SKIPIF — ПРОПУСТИТЬ ПО УСЛОВИЮ
# ============================================================

@pytest.mark.skipif(sys.version_info < (3, 8), reason="Требуется Python 3.8+")
def test_requires_python38():
    """Тест запустится только на Python 3.8+."""
    # walrus operator (:=) появился в Python 3.8
    result = (x := 42)
    assert result == 42


@pytest.mark.skipif(sys.platform == "win32", reason="Не работает на Windows")
def test_unix_only():
    """Этот тест пропущен на Windows."""
    import os
    assert os.name == "posix"


# ============================================================
# XFAIL — ОЖИДАЕМОЕ ПАДЕНИЕ
# ============================================================

@pytest.mark.xfail(reason="Известный баг #42 — деление на ноль")
def test_known_bug():
    """Тест УПАДЁТ, но это ожидаемо — тест помечается как XPASS/XFAIL."""
    assert 1 / 0  # Упадёт, но мы знаем об этом


@pytest.mark.xfail(reason="Баг исправлен, но тест ещё не обновили")
def test_fixed_bug():
    """
    Тест НЕ упадёт (потому что баг исправлен).
    Pytest сообщит: XPASS (unexpectedly passed) — неожиданный успех.
    """
    assert 2 + 2 == 4  # Не падает!


@pytest.mark.xfail(strict=True, reason="Строгий режим: должен УПАСТЬ")
def test_strict_xfail():
    """
    strict=True — если тест НЕ упадёт, это будет считаться ОШИБКОЙ.
    """
    # assert 1 == 2  # раскомментируйте чтобы тест падал как ожидается
    assert 1 == 1  # Это вызовет ОШИБКУ (должен был упасть, но прошёл!)


# ============================================================
# КАСТОМНЫЕ МАРКЕРЫ
# ============================================================

@pytest.mark.smoke
def test_smoke_login():
    """Smoke-тест: проверка входа (критическая функциональность)."""
    assert True


@pytest.mark.smoke
def test_smoke_homepage():
    """Smoke-тест: главная страница загружается."""
    assert True


@pytest.mark.regression
def test_regression_feature_x():
    """Регрессионный тест."""
    assert True


@pytest.mark.slow
def test_slow_operation():
    """Медленный тест — можно исключить из быстрого прогона."""
    import time
    time.sleep(0.1)  # эмуляция медленной операции
    assert True


@pytest.mark.fast
def test_fast_check():
    """Быстрый тест."""
    assert True


@pytest.mark.bug
def test_bug_tracker_123():
    """Тест для бага #123 из трекера."""
    # Когда баг исправят — тест начнёт проходить
    assert True


# ============================================================
# КОМБИНИРОВАНИЕ МАРКЕРОВ
# ============================================================

@pytest.mark.smoke
@pytest.mark.fast
def test_critical_fast():
    """Критический И быстрый тест."""
    assert True


# ============================================================
# ЗАПУСК ТЕСТОВ С МАРКЕРАМИ
# ============================================================

"""
Запуск по маркерам:

    pytest -m "smoke"              # Только smoke
    pytest -m "not slow"           # Все, кроме slow
    pytest -m "smoke and fast"     # Smoke И fast
    pytest -m "smoke or regression" # Smoke ИЛИ regression
    pytest -m "not (slow or bug)"  # Не slow и не bug
"""
