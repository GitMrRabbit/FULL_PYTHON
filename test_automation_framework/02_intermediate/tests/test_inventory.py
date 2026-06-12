"""Тесты страницы товаров (Inventory)."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from factories.user_factory import UserFactory


class TestInventory:
    """Тесты для страницы товаров SauceDemo."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Логин перед каждым тестом."""
        self.driver = driver
        user = UserFactory.standard_user()
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(user.username, user.password)
        self.inventory = InventoryPage(self.driver)
        self.inventory.wait_for_load()

    @pytest.mark.smoke
    def test_inventory_page_loaded(self):
        """Проверка загрузки страницы товаров."""
        assert self.inventory.is_loaded(), "Страница товаров не загрузилась"
        assert "Products" in self.inventory.get_title()

    @pytest.mark.inventory
    def test_products_displayed(self):
        """Проверка отображения товаров."""
        count = self.inventory.get_product_count()
        assert count > 0, "Товары не отображаются"

    @pytest.mark.inventory
    def test_add_product_to_cart(self):
        """Добавление товара в корзину."""
        self.inventory.add_product_to_cart("Sauce Labs Backpack")
        assert self.inventory.get_cart_count() == 1, "Счётчик корзины не обновился"

    @pytest.mark.inventory
    def test_add_multiple_products(self):
        """Добавление нескольких товаров."""
        self.inventory.add_products(
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light"
        )
        assert self.inventory.get_cart_count() == 2

    @pytest.mark.inventory
    def test_remove_product_from_cart(self):
        """Удаление товара из корзины со страницы товаров."""
        self.inventory.add_product_to_cart("Sauce Labs Backpack")
        assert self.inventory.get_cart_count() == 1
        self.inventory.remove_product_from_cart("Sauce Labs Backpack")
        assert self.inventory.get_cart_count() == 0

    @pytest.mark.smoke
    def test_navigate_to_cart(self):
        """Переход в корзину."""
        self.inventory.go_to_cart()
        assert "cart" in self.driver.current_url.lower()
