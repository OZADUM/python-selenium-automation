# pages/help_page.py
from .base_page import Page
from urllib.parse import quote_plus

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HelpPage(Page):
    BASE_URL = "https://www.target.com/help"
    RETURNS_URL = "https://www.target.com/help/topic-page/returns"

    TOPIC_QUERY_MAP = {
        "Returns": "childcat=Returns",
        "Returns & Exchanges": "parentcat=Returns+%26+Exchanges",
        "Promotions & Coupons": "childcat=Promotions+%26+Coupons",
        "Target Circle": "childcat=Target+Circle",
        "Target Circle™": "childcat=Target+Circle",
    }

    _DROPDOWN_BUTTONS = (
        By.CSS_SELECTOR,
        'button[data-test*="help"][aria-haspopup="menu"], '
        'button[data-test*="topic"], '
        'button[aria-haspopup="menu"], '
        '[data-test*="dropdown"], '
        '[aria-controls*="menu"]',
    )
    _MENU_ITEMS = (
        By.CSS_SELECTOR,
        '[role="menuitem"], '
        '[data-test*="option"], '
        'a[role="menuitem"], '
        'a[href*="help"]',
    )

    # ----- Navigation -----
    def open_help(self):
        self.driver.get(self.BASE_URL)

    def open_help_returns(self):
        self.driver.get(self.RETURNS_URL)

    # ----- Assertions -----
    def assert_url_contains(self, fragment: str, timeout: int = 12):
        WebDriverWait(self.driver, timeout).until(
            lambda d: fragment in d.current_url
        ), f"Expected URL to contain '{fragment}', got: {self.driver.current_url}"

    def assert_url_contains_ci(self, fragment: str, timeout: int = 12):
        f = fragment.lower()
        WebDriverWait(self.driver, timeout).until(
            lambda d: f in d.current_url.lower()
        ), f"Expected URL to contain '{fragment}' (CI), got: {self.driver.current_url}"

    def assert_url_contains_any_ci(self, fragments: list[str], timeout: int = 12):
        def ok(d):
            url = d.current_url.lower()
            return any(f.lower() in url for f in fragments)
        WebDriverWait(self.driver, timeout).until(ok), \
            f"Expected URL to contain one of {fragments} (CI), got: {self.driver.current_url}"

    # ----- Public API -----
    def select_topic(self, topic_text: str, timeout_click: int = 3):
        if self._try_ui_select(topic_text, timeout_click):
            return
        self._navigate_by_topic_map(topic_text)

    # ----- Internals -----
    def _try_ui_select(self, topic_text: str, timeout_click: int) -> bool:
        wait = WebDriverWait(self.driver, timeout_click)

        try:
            dropdown = wait.until(EC.element_to_be_clickable(self._DROPDOWN_BUTTONS))
            dropdown.click()
            options = wait.until(EC.presence_of_all_elements_located(self._MENU_ITEMS))
            want = topic_text.strip().lower()
            for opt in options:
                if want in opt.text.strip().lower():
                    wait.until(EC.element_to_be_clickable(opt)).click()
                    return True
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
            pass

        try:
            lowered = topic_text.strip().lower().replace("&", "and").replace("™", "")
            xpath = (
                f'//a[contains(translate(normalize-space(.), '
                f'"ABCDEFGHIJKLMNOPQRSTUVWXYZ™", "abcdefghijklmnopqrstuvwxyz"), '
                f'"{lowered}")]'
            )
            link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            link.click()
            return True
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
            return False

    def _navigate_by_topic_map(self, topic_text: str):
        fragment = self._lookup_fragment(topic_text)
        self.driver.get(f"{self.BASE_URL}?{fragment}")

    def _lookup_fragment(self, topic_text: str) -> str:
        for k in {topic_text, topic_text.replace('™', '').strip(), topic_text.replace('&', 'and').strip()}:
            if k in self.TOPIC_QUERY_MAP:
                return self.TOPIC_QUERY_MAP[k]
        return f"childcat={quote_plus(topic_text.replace('™', '').strip())}"