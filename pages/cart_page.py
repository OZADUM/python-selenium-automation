from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.base_page import Page


class CartPage(Page):
    """
    Page Object for Target cart.

    Goals:
    - Open /cart and wait for a stable render signal (empty, items, or subtotal)
    - Count cart line items robustly
    - Verify presence of an expected product title
    """

    URL = "https://www.target.com/cart"

    # Signals/locators
    CART_EMPTY_MSG = (By.CSS_SELECTOR, "[data-test='boxEmptyMsg']")
    # Some carts render <li data-test="cartItem">, so include both
    CART_ITEMS = (By.CSS_SELECTOR, "[data-test='cartItem'], li[data-test='cartItem']")
    CART_ITEM_TITLE = (By.CSS_SELECTOR, "[data-test='cartItem-title']")
    SUBTOTAL = (By.XPATH, "//div[./span[contains(translate(.,"
                          "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
                          "'subtotal')]]")

    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, timeout)

    # ---------- Navigation ----------

    def open(self):
        """Navigate to the cart page and wait for a stable render signal."""
        if not self.driver.current_url.startswith(self.URL):
            self.driver.get(self.URL)

        # Ensure URL is correct first (helps on slow redirects)
        try:
            self.wait.until(EC.url_contains("/cart"))
        except TimeoutException:
            # Continue anyway; verify_* methods will assert precisely
            pass

        # Wait for either: at least one line item, the empty-cart message, or the subtotal block
        try:
            self.wait.until(
                lambda d: d.find_elements(*self.CART_ITEMS)
                          or d.find_elements(*self.CART_EMPTY_MSG)
                          or d.find_elements(*self.SUBTOTAL)
            )
        except TimeoutException:
            # Don't fail here; verification methods provide clearer errors
            pass

    # ---------- Queries ----------

    def get_items_count(self) -> int:
        """
        Return the number of line items in the cart.
        Falls back to parsing the subtotal block if rows are not yet present.
        """
        items = self.driver.find_elements(*self.CART_ITEMS)
        if items:
            return len(items)

        # Fallback: sometimes rows are virtualized/delayed; parse “… item(s)” from subtotal text.
        try:
            subtotal_text = self.driver.find_element(*self.SUBTOTAL).text.lower()
            # crude parse; handles “1 item” / “2 items” etc.
            for token in subtotal_text.split():
                if token.isdigit():
                    return int(token)
        except Exception:
            pass

        return 0

    def get_all_titles(self):
        """Return list of product titles currently in cart (non-empty)."""
        return [el.text.strip()
                for el in self.driver.find_elements(*self.CART_ITEM_TITLE)
                if el.text.strip()]

    # ---------- Assertions ----------

    def verify_cart_empty_msg(self):
        """Assert the empty-cart message is visible."""
        self.verify_text("Your cart is empty", *self.CART_EMPTY_MSG)

    def verify_items_count(self, expected: int):
        """Assert the cart contains the expected number of items."""
        actual = self.get_items_count()
        if actual != expected:
            titles = self.get_all_titles()
            raise AssertionError(
                f"Expected {expected} items but got {actual}. "
                f"Titles seen: {titles} | URL: {self.driver.current_url}"
            )

    def verify_contains_product(self, expected_name_substring: str):
        """
        Assert that any cart item title contains the expected substring
        (case-insensitive). Helpful for long vendor titles.
        """
        titles = self.get_all_titles()
        haystack = " | ".join(titles).lower()
        needle = (expected_name_substring or "").lower().strip()

        assert needle, "Expected product name is empty."
        assert needle in haystack, (
            f"Cart does not contain expected product: '{expected_name_substring}'. "
            f"Found titles: {titles}"
        )