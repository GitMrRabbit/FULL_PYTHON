"""
config_manager.py — Загрузчик конфигурации из YAML-файла.

Демонстрирует:
- Чтение YAML-конфигурации
- Доступ к настройкам через точку (dot notation)
- Значения по умолчанию
"""

import yaml
import os
from pathlib import Path


class ConfigManager:
    """
    Управление конфигурацией тестового фреймворка.
    
    Загружает настройки из YAML-файла и предоставляет
    удобный доступ к ним через атрибуты.
    """
    
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key, default=None):
        """Получить значение по ключу (поддержка вложенных через точку)."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value
    
    @property
    def base_url(self):
        return self.get('app.base_url', 'https://www.saucedemo.com')
    
    @property
    def browser(self):
        return self.get('browser', 'chrome')
    
    @property
    def timeout(self):
        return self.get('timeout', 10)
    
    @property
    def headless(self):
        return self.get('headless', False)


# Singleton — единственный экземпляр конфигурации
config = ConfigManager()
