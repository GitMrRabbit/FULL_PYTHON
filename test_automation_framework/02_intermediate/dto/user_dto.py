"""
user_dto.py — Data Transfer Object (DTO) для пользователя.

DTO — простой объект для передачи данных между слоями приложения.
Не содержит бизнес-логики, только данные.

Демонстрирует:
- dataclass (Python 3.7+) — минимальный код для DTO
- Валидацию данных
- Сериализацию в словарь
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class UserDTO:
    """
    DTO для представления пользователя.
    
    Используется для:
    - Передачи тестовых данных в тесты
    - Сериализации/десериализации (JSON, YAML, БД)
    - Отделения данных от бизнес-логики
    """
    username: str
    password: str
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    is_locked: bool = False
    
    def to_dict(self) -> dict:
        """Сериализовать в словарь."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "UserDTO":
        """Создать DTO из словаря."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    @property
    def full_name(self) -> str:
        """Полное имя пользователя."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def __post_init__(self):
        """Валидация после инициализации."""
        if not self.username:
            raise ValueError("Имя пользователя не может быть пустым")
        if not self.password:
            raise ValueError("Пароль не может быть пустым")


# Предопределённые пользователи (как в SauceDemo)
STANDARD_USER = UserDTO(
    username="standard_user",
    password="secret_sauce",
    first_name="Standard",
    last_name="User"
)

LOCKED_OUT_USER = UserDTO(
    username="locked_out_user",
    password="secret_sauce",
    first_name="Locked",
    last_name="Out",
    is_locked=True
)

PROBLEM_USER = UserDTO(
    username="problem_user",
    password="secret_sauce",
    first_name="Problem",
    last_name="User"
)

PERFORMANCE_GLITCH_USER = UserDTO(
    username="performance_glitch_user",
    password="secret_sauce",
    first_name="Performance",
    last_name="Glitch"
)
