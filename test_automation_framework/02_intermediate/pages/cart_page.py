"""Page Object для корзины (SauceDemo Cart)."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Страница корзины."""

    URL = "https://www.saucedemo.com/cart.html"

    TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    @staticmethod
    def remove_button(product_name: str) -> tuple:
        return (By.XPATH,
                f"//div[text()='{product_name}']/"
                f"ancestor::div[@class='cart_item']//button")

    def is_loaded(self) -> bool:
        return self.is_element_visible(self.TITLE)

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_item(self, product_name: str) -> None:
        self.click(self.remove_button(product_name))

    def go_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING)

    def is_empty(self) -> bool:
        return self.get_item_count() == 0
