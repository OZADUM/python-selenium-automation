from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pages.base_page import Page


class HelpPage(Page):
    """
    Target Help POM with resilient dropdown selection:
    - fuzzy match by visible text (case-insensitive, substring OK)
    - fallback to select_by_value if text not found
    """

    # Dynamic header <h1> text
    HEADER = (By.XPATH, "//h1[normalize-space() = '{SUBSTR}']")

    # Topic dropdown (Lesson 9 used an id containing 'ViewHelpTopics')
    SELECT_TOPIC_DD = (By.CSS_SELECTOR, "select[id*='ViewHelpTopics'], select")

    DEFAULT_RETURNS_URL = (
        "https://help.target.com/help/SubCategoryArticle"
        "?childcat=Returns&parentcat=Returns+%26+Exchanges"
    )

    # ---- utils ----
    def get_locator(self, expected_header_text: str):
        return [self.HEADER[0], self.HEADER[1].replace("{SUBSTR}", expected_header_text)]

    def _dropdown(self) -> Select:
        dd = self.find_element(*self.SELECT_TOPIC_DD)
        return Select(dd)

    def _normalize(self, s: str) -> str:
        return " ".join(s.split()).strip().lower()

    # ---- navigation ----
    def open_help(self, url: str | None = None):
        self.driver.get(url or self.DEFAULT_RETURNS_URL)
        self.wait_until_element_appear(*self.SELECT_TOPIC_DD)

    def open_help_returns(self):
        self.open_help(self.DEFAULT_RETURNS_URL)

    # ---- interactions ----
    def select_topic_fuzzy(self, topic_text: str, wait_for_url_contains: str | None = None):
        """
        Select an option whose VISIBLE TEXT contains topic_text (case-insensitive).
        If no visible text matches, try value attribute contains topic_text.
        """
        sel = self._dropdown()
        target = self._normalize(topic_text)

        # 1) try by visible text (substring, case-insensitive)
        options = sel.options
        for opt in options:
            txt = self._normalize(opt.text)
            if target in txt:
                sel.select_by_visible_text(opt.text)
                break
        else:
            # 2) fallback: try value attribute substring match
            matched = False
            for opt in options:
                val = (opt.get_attribute("value") or "")
                if target in self._normalize(val):
                    sel.select_by_value(val)
                    matched = True
                    break
            if not matched:
                raise NoSuchElementException(f"Help topic not found (by text or value): {topic_text}")

        # Optional URL wait (some pages navigate after selection)
        if wait_for_url_contains:
            self.wait.until(lambda d: wait_for_url_contains in d.current_url)

    def select_topic_by_text(self, topic_text: str, wait_for_url_contains: str | None = None):
        """Exact visible-text selection (legacy)."""
        self._dropdown().select_by_visible_text(topic_text)
        if wait_for_url_contains:
            self.wait.until(lambda d: wait_for_url_contains in d.current_url)

    def select_topic_by_value(self, value: str, wait_for_url_contains: str | None = None):
        """Exact value selection (legacy)."""
        self._dropdown().select_by_value(value)
        if wait_for_url_contains:
            self.wait.until(lambda d: wait_for_url_contains in d.current_url)

    # ---- verification ----
    def verify_header(self, expected_header_text: str):
        locator = self.get_locator(expected_header_text)
        self.wait_until_element_appear(*locator)

    def verify_url_contains(self, expected_fragment: str):
        try:
            self.wait.until(lambda d: expected_fragment in d.current_url)
        except TimeoutException:
            raise AssertionError(
                f"Expected '{expected_fragment}' in URL, got: {self.driver.current_url}"
            )