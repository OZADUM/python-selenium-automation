# pages/cart_page.py
from __future__ import annotations

from typing import List, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import Page


class CartPage(Page):
    """
    Target Cart page object.

    Goals:
    - Be resilient to minor DOM changes (use multiple locators / fallbacks).
    - Provide simple, intention-revealing helpers the steps can call.
    """

    # ---- Common locators (broad on purpose) ---------------------------------
    # Cart line items (try several common DOM hooks)
    CART_LINES = (
        By.CSS_SELECTOR,
        "[data-test='cartItem'], [data-test='cartItemLine'], li[data-test*='cart'] div[data-test*='item']",
    )

    # Titles inside cart lines (again: a few variants)
    CART_TITLES = (
        By.CSS_SELECTOR,
        "[data-test='cart-item-title'], [data-test='item-title'], a[data-test='cartItem-title'], h3, h2",
    )

    # Generic 'empty' text check (fallback to page_source for robustness)
    EMPTY_TEXT_XPATH = (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), \"your cart is empty\")]")

    # -------------------------------------------------------------------------

    def open_cart(self) -> None:
        """Open the cart page directly (stable URL)."""
        self.open_url("https://www.target.com/cart")

    # ---- Reads ----------------------------------------------------------------

    def _find_all(self, by: By, value: str) -> List:
        els = self.find_elements(by, value)
        return [e for e in els if e.is_displayed()]

    def get_cart_lines(self) -> List:
        return self._find_all(*self.CART_LINES)

    def get_cart_titles(self) -> List[str]:
        titles = []
        for e in self._find_all(*self.CART_TITLES):
            txt = (e.text or "").strip()
            if txt:
                titles.append(txt)
        # De-dupe while preserving order
        seen = set()
        unique = []
        for t in titles:
            if t not in seen:
                seen.add(t)
                unique.append(t)
        return unique

    # ---- Assertions -----------------------------------------------------------

    def assert_items_count(self, expected: int, timeout: int = 10) -> None:
        """Wait until we see expected number of cart lines."""
        def _ok(drv):
            return len(self.get_cart_lines()) == expected

        WebDriverWait(self.driver, timeout).until(_ok), \
            f"Expected {expected} item(s) in cart, saw {len(self.get_cart_lines())}."

    def assert_cart_contains_name(self, expected: str) -> None:
        """
        Check that at least one cart line's title contains the expected name.
        Tolerates vendor suffix (split by '|') and minor variations.
        """
        titles = self.get_cart_titles()
        base_expected = expected.split("|")[0].strip()
        assert any(
            base_expected in t or expected in t
            for t in titles
        ), f"Expected product '{expected}' not found in cart titles: {titles}"

    def wait_until_empty(self, timeout: int = 6) -> bool:
        """Return True when the cart looks empty (text or page_source)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: (
                    len(self.get_cart_lines()) == 0
                    or bool(self.find_elements(*self.EMPTY_TEXT_XPATH))
                    or ("your cart is empty" in d.page_source.lower())
                )
            )
            return True
        except Exception:
            return False