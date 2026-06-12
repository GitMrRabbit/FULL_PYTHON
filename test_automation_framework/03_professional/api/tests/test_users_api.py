"""
test_users_api.py — API тесты с Pydantic моделями

Демонстрирует:
- API тестирование с requests
- Валидацию ответов через Pydantic
- Проверку status code, заголовков, тела ответа
- Параметризованные API тесты
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from common.api_client import ApiClient
from api.models.user_model import UserModel


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def api():
    """
    Фикстура API клиента на уровне модуля.
    
    Один клиент для всех тестов в модуле (переиспользуем сессию).
    """
    client = ApiClient(base_url="https://jsonplaceholder.typicode.com")
    yield client
    client.close()


# ============================================================
# ТЕСТЫ
# ============================================================

class TestUsersAPI:
    """API тесты для эндпоинта /users."""
    
    def test_get_all_users(self, api):
        """
        GET /users — получить всех пользователей.
        
        Проверяем:
        - Status code 200
        - Content-Type: application/json
        - Ответ — список из 10 пользователей
        - Каждый пользователь валидируется через Pydantic
        """
        response = api.get("/users")
        
        # Проверка HTTP статуса
        assert response.status_code == 200, \
            f"Ожидался 200, получен {response.status_code}"
        
        # Проверка Content-Type
        assert "application/json" in response.headers["Content-Type"]
        
        # Парсим JSON
        users_data = response.json()
        
        # Проверяем, что это список
        assert isinstance(users_data, list)
        assert len(users_data) == 10
        
        # Валидируем каждого пользователя через Pydantic
        for user_data in users_data:
            user = UserModel(**user_data)
            assert user.id > 0
            assert "@" in user.email
    
    def test_get_single_user(self, api):
        """
        GET /users/1 — получить одного пользователя.
        
        Проверяем:
        - Status code 200
        - Pydantic валидация
        - Конкретные поля
        """
        response = api.get("/users/1")
        
        assert response.status_code == 200
        
        # Валидация через Pydantic
        user = UserModel(**response.json())
        
        assert user.id == 1
        assert user.name == "Leanne Graham"
        assert user.username == "Bret"
        assert "april.biz" in user.email
    
    def test_get_nonexistent_user(self, api):
        """
        GET /users/999 — несуществующий пользователь.
        
        Проверяем:
        - Status code 404
        """
        response = api.get("/users/999")
        assert response.status_code == 404
    
    def test_create_user(self, api):
        """
        POST /users — создать пользователя.
        
        Проверяем:
        - Status code 201
        - Ответ содержит переданные данные
        - id присвоен
        """
        new_user_data = {
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com"
        }
        
        response = api.post("/users", json=new_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test User"
        assert data["username"] == "testuser"
        assert "id" in data  # должен быть присвоен сервером
    
    def test_response_headers(self, api):
        """Проверка заголовков ответа."""
        response = api.get("/users")
        
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"
        assert "Content-Length" in response.headers
        assert int(response.headers["Content-Length"]) > 0


@pytest.mark.parametrize("user_id,expected_name", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
    (3, "Clementine Bauch"),
])
def test_users_by_id(api, user_id, expected_name):
    """
    Параметризованный тест: проверка нескольких пользователей.
    """
    response = api.get(f"/users/{user_id}")
    assert response.status_code == 200
    
    user = UserModel(**response.json())
    assert user.name == expected_name
