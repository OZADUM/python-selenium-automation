from selenium.webdriver.common.by import By
from pages.base_page import Page

class CartPage(Page):
    CART_EMPTY_MSG = (By.CSS_SELECTOR, "[data-test='boxEmptyMsg'], [data-test='@web/Cart/EmptyBox']")

    def open_cart(self):
        self.open_url("https://www.target.com/cart")

    def verify_cart_empty_message(self):
        msg = self.get_text(self.CART_EMPTY_MSG).strip().lower()
        assert "empty" in msg, f"Expected 'empty' message, got: {msg!r}"