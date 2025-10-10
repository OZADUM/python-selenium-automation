from selenium.webdriver.common.by import By
from time import sleep

from pages.base_page import Page


class Header(Page):
    CART_ICON = (By.CSS_SELECTOR, '[data-test="@web/CartLink"]')
    SEARCH_FIELD = (By.ID, 'search')
    SEARCH_BTN = (By.XPATH, "//button[@data-test='@web/Search/SearchButton']")

    # Primary selector covers multiple Target variants (comma-separated CSS = OR)
    SIGN_IN_BTN = (
        By.CSS_SELECTOR,
        "[data-test='@web/AccountLink'], "
        "[data-test='accountNav-button'], "
        "[data-test='accountNavButton']"
    )

    # Conservative text-based fallback if data-test changes
    SIGN_IN_FALLBACK = (
        By.XPATH,
        "//button[.//span[normalize-space()='Sign in'] or normalize-space()='Sign in']"
        " | //a[normalize-space()='Sign in']"
    )

    def search_product(self, search_word: str):
        self.input_text(search_word, *self.SEARCH_FIELD)
        self.click(*self.SEARCH_BTN)
        # TODO: replace sleep with an explicit wait for results (see note below)
        sleep(9)

    def click_cart(self):
        self.wait_until_clickable_click(*self.CART_ICON)

    # Click the header “Sign in” to open the right-side sheet
    def click_sign_in(self):
        try:
            self.wait_until_clickable_click(*self.SIGN_IN_BTN)
        except Exception:
            self.wait_until_clickable_click(*self.SIGN_IN_FALLBACK)