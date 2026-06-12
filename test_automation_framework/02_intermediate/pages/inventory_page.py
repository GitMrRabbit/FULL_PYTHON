"""Page Object для страницы товаров (SauceDemo Inventory)."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Страница со списком товаров."""

    URL = "https://www.saucedemo.com/inventory.html"

    # Locators
    TITLE = (By.CLASS_NAME, "title")
    PRODUCT_SORT = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")

    @staticmethod
    def product_add_button(product_name: str) -> tuple:
        """Локатор кнопки 'Add to cart' для товара по имени."""
        return (By.XPATH,
                f"//div[text()='{product_name}']/"
                f"ancestor::div[@class='inventory_item']//button")

    @staticmethod
    def product_remove_button(product_name: str) -> tuple:
        return (By.XPATH,
                f"//div[text()='{product_name}']/"
                f"ancestor::div[@class='inventory_item']//button[text()='Remove']")

    def is_loaded(self) -> bool:
        return self.is_element_visible(self.TITLE)

    def get_title(self) -> str:
        return self.get_text(self.TITLE)

    def get_cart_count(self) -> int:
        try:
            return int(self.get_text(self.SHOPPING_CART_BADGE))
        except Exception:
            return 0

    def add_product_to_cart(self, product_name: str) -> None:
        self.click(self.product_add_button(product_name))

    def remove_product_from_cart(self, product_name: str) -> None:
        self.click(self.product_remove_button(product_name))

    def go_to_cart(self) -> None:
        self.click(self.SHOPPING_CART_LINK)

    def add_products(self, *product_names: str) -> None:
        for name in product_names:
            self.add_product_to_cart(name)

    def get_product_count(self) -> int:
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        return len(items)
