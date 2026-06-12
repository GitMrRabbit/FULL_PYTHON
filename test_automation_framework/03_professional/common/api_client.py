"""
api_client.py — Профессиональный HTTP клиент с retry, таймаутами, логированием.

Демонстрирует:
- Сессии с повторным использованием соединений
- Автоматический retry при ошибках сети
- Таймауты
- Логирование запросов/ответов
- Базовые HTTP методы с обработкой ошибок
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

logger = logging.getLogger(__name__)


class ApiClient:
    """
    Профессиональный HTTP клиент.
    
    Особенности:
    - Connection pooling (переиспользование соединений)
    - Автоматический retry (3 попытки с exponential backoff)
    - Таймауты (connect + read)
    - Логирование всех запросов
    - Поддержка базовой аутентификации и токенов
    """
    
    def __init__(self, base_url, timeout=30, retries=3, auth=None):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Настройка auth
        if auth:
            if isinstance(auth, tuple):
                self.session.auth = auth
            elif isinstance(auth, str):
                self.session.headers["Authorization"] = f"Bearer {auth}"
        
        # Настройка retry
        retry_strategy = Retry(
            total=retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _build_url(self, endpoint):
        """Собрать полный URL."""
        return f"{self.base_url}/{endpoint.lstrip('/')}"
    
    def _log_request(self, method, url, **kwargs):
        """Логировать запрос."""
        logger.info(f"→ {method} {url}")
        if 'json' in kwargs:
            logger.debug(f"  Body: {kwargs['json']}")
    
    def _log_response(self, response):
        """Логировать ответ."""
        logger.info(f"← {response.status_code} ({len(response.content)} bytes)")
        if not response.ok:
            logger.warning(f"  Response: {response.text[:500]}")
    
    def request(self, method, endpoint, **kwargs):
        """
        Выполнить HTTP запрос.
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE, PATCH)
            endpoint: путь (например, '/users')
            **kwargs: дополнительные параметры для requests
        """
        url = self._build_url(endpoint)
        kwargs.setdefault('timeout', self.timeout)
        
        self._log_request(method, url, **kwargs)
        
        response = self.session.request(method, url, **kwargs)
        
        self._log_response(response)
        
        # Проверка на ошибки
        if response.status_code >= 400:
            logger.error(f"HTTP {response.status_code}: {response.text[:500]}")
        
        return response
    
    def get(self, endpoint, **kwargs):
        """GET запрос."""
        return self.request('GET', endpoint, **kwargs)
    
    def post(self, endpoint, **kwargs):
        """POST запрос."""
        return self.request('POST', endpoint, **kwargs)
    
    def put(self, endpoint, **kwargs):
        """PUT запрос."""
        return self.request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """DELETE запрос."""
        return self.request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint, **kwargs):
        """PATCH запрос."""
        return self.request('PATCH', endpoint, **kwargs)
    
    def close(self):
        """Закрыть сессию."""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
