"""Тесты корзины."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from factories.user_factory import UserFactory


class TestCart:
    """Тесты корзины."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        user = UserFactory.standard_user()
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(user.username, user.password)
        self.inventory = InventoryPage(self.driver)
        self.inventory.wait_for_load()
        self.cart = CartPage(self.driver)

    @pytest.mark.cart
    def test_empty_cart(self):
        """Проверка пустой корзины."""
        self.inventory.go_to_cart()
        self.cart.wait_for_load()
        assert self.cart.is_empty(), "Корзина должна быть пустой"

    @pytest.mark.cart
    def test_add_and_remove_item(self):
        """Добавление и удаление товара в корзине."""
        self.inventory.add_product_to_cart("Sauce Labs Backpack")
        self.inventory.go_to_cart()
        self.cart.wait_for_load()
        assert self.cart.get_item_count() == 1
        self.cart.remove_item("Sauce Labs Backpack")
        assert self.cart.is_empty()

    @pytest.mark.cart
    @pytest.mark.smoke
    def test_proceed_to_checkout(self):
        """Переход к оформлению заказа."""
        self.inventory.add_product_to_cart("Sauce Labs Backpack")
        self.inventory.go_to_cart()
        self.cart.wait_for_load()
        self.cart.go_to_checkout()
        assert "checkout" in self.driver.current_url.lower()

    @pytest.mark.cart
    def test_continue_shopping(self):
        """Возврат к покупкам из корзины."""
        self.inventory.add_product_to_cart("Sauce Labs Backpack")
        self.inventory.go_to_cart()
        self.cart.wait_for_load()
        self.cart.continue_shopping()
        assert "inventory" in self.driver.current_url.lower()
