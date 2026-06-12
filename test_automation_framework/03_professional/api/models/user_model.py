"""
user_model.py — Pydantic модели для API

Демонстрирует:
- Pydantic BaseModel для валидации API ответов
- Автоматическую сериализацию/десериализацию
- Валидацию типов данных
- Кастомные валидаторы
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class GeoLocation(BaseModel):
    """Гео-локация пользователя."""
    lat: str
    lng: str


class Address(BaseModel):
    """Адрес пользователя."""
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoLocation


class Company(BaseModel):
    """Информация о компании."""
    name: str
    catchPhrase: str
    bs: str


class UserModel(BaseModel):
    """
    Pydantic модель пользователя из JSONPlaceholder API.
    
    Автоматически:
    - Валидирует типы
    - Преобразует данные
    - Сериализует в JSON
    """
    id: int
    name: str = Field(..., min_length=2, description="Полное имя пользователя")
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Кастомная валидация email."""
        if '@' not in v:
            raise ValueError('Некорректный email')
        return v.lower()
    
    @property
    def full_address(self) -> str:
        """Полный адрес одной строкой."""
        a = self.address
        return f"{a.street}, {a.suite}, {a.city}, {a.zipcode}"
    
    class Config:
        """Дополнительная конфигурация."""
        # Разрешить передачу лишних полей (игнорировать их)
        extra = "ignore"
        # Пример для генерации схемы
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Leanne Graham",
                "username": "Bret",
                "email": "Sincere@april.biz",
                "address": {
                    "street": "Kulas Light",
                    "suite": "Apt. 556",
                    "city": "Gwenborough",
                    "zipcode": "92998-3874",
                    "geo": {"lat": "-37.3159", "lng": "81.1496"}
                },
                "phone": "1-770-736-8031 x56442",
                "website": "hildegard.org",
                "company": {
                    "name": "Romaguera-Crona",
                    "catchPhrase": "Multi-layered client-server neural-net",
                    "bs": "harness real-time e-markets"
                }
            }
        }


class UserListResponse(BaseModel):
    """Модель ответа со списком пользователей."""
    users: List[UserModel]
    total: int = 0
