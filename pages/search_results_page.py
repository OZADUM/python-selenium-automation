# pages/search_results_page.py
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import Page


class SearchResultsPage(Page):
    """
    Target search results page object with resilient locators.
    """

    # A result tile (fairly broad)
    RESULT_TILES = (
        By.CSS_SELECTOR,
        "[data-test='productGridItem'],[data-test*='productCard'],li[data-test*='result']"
    )

    # Title inside a tile
    TILE_TITLE = (
        By.CSS_SELECTOR,
        "[data-test='product-title'],[data-test='product-title-link'],a[title],h3,h2"
    )

    # The primary Add-to-cart button inside a tile
    TILE_ADD_TO_CART = (
        By.CSS_SELECTOR,
        "button[data-test='addToCartButton'], button[aria-label*='Add to cart'], button:has(span:contains('Add to cart'))"
    )

    # Results header that typically echoes the query (fallback to any <h1>)
    RESULTS_HEADER = (By.CSS_SELECTOR, "[data-test='resultsHeading'], h1")

    # Side sheet confirmation / go-to-cart actions (try several)
    SIDE_SHEET_VIEW_CART = (
        By.XPATH,
        "//a//span[contains(., 'View cart') or contains(., 'Checkout')]/ancestor::a | "
        "//button//span[contains(., 'View cart') or contains(., 'Checkout')]/ancestor::button"
    )

    def _first_visible(self, by, value, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(e.is_displayed() for e in d.find_elements(by, value)),
            "No visible result tiles found."
        )
        for e in self.find_elements(by, value):
            if e.is_displayed():
                return e
        return None

    # ---- Actions -------------------------------------------------------------

    def click_first_add_to_cart(self) -> None:
        tile = self._first_visible(*self.RESULT_TILES)
        assert tile, "No visible product tiles to click Add to cart."
        # Try to find the add-to-cart within that tile; if not, fallback globally
        btns = tile.find_elements(*self.TILE_ADD_TO_CART)
        if not btns:
            btns = self.find_elements(*self.TILE_ADD_TO_CART)
        assert btns, "Could not find an 'Add to cart' button."
        btns[0].click()

    def get_first_result_title(self) -> str:
        tile = self._first_visible(*self.RESULT_TILES)
        assert tile, "No visible product tiles to read title."
        # Prefer an inner title
        titles = tile.find_elements(*self.TILE_TITLE)
        text = ""
        for t in titles:
            text = (t.get_attribute("title") or t.text or "").strip()
            if text:
                break
        assert text, "Could not read product title from first result tile."
        return text

    def confirm_from_side_sheet(self) -> None:
        """
        Click 'View cart & checkout' (or similar) when the side sheet appears.
        If it never appears, this just returns (no-op), allowing flows that jump directly.
        """
        try:
            btn = WebDriverWait(self.driver, 6).until(
                EC.element_to_be_clickable(self.SIDE_SHEET_VIEW_CART)
            )
            btn.click()
        except Exception:
            # Side sheet didn't appear – that's OK for some flows
            pass

    # ---- Assertions ----------------------------------------------------------

    def assert_results_for(self, query: str) -> None:
        try:
            hdr = WebDriverWait(self.driver, 8).until(
                EC.visibility_of_element_located(self.RESULTS_HEADER)
            )
            text = (hdr.text or "").lower()
            assert query.lower() in text, f"Results header didn't mention '{query}'. Got: '{hdr.text}'"
        except Exception:
            # Very defensive fallback
            assert query.lower() in self.driver.page_source.lower(), \
                f"Search results page source didn't mention '{query}'."