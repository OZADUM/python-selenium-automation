# pages/help_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions as SELex
from urllib.parse import quote_plus


class HelpPage:
    # ---------- Canonical URLs ----------
    HELP_URL_RETURNS = (
        "https://help.target.com/help/subcategoryarticle?parentcat=Returns+%26+Exchanges"
    )

    DIRECT_TOPIC_URLS = {
        "Promotions & Coupons": "https://help.target.com/help/subcategoryarticle?parentcat=Promotions+%26+Coupons",
        "Target Circle": "https://help.target.com/help/subcategoryarticle?parentcat=Target+Circle",
        "Target Circle™": "https://help.target.com/help/subcategoryarticle?parentcat=Target+Circle",
    }

    # ---------- Locators ----------
    _TOPIC_DROPDOWN = (
        By.XPATH,
        "//select[@id='helpTopic' or contains(@aria-label,'Help topics') or contains(@name,'topic')]",
    )
    _PAGE_TITLE = (By.XPATH, "//h1 | //header//h1 | //*[@data-test='help-article-title']")

    def _topic_option_by_text(self, topic):
        topic_norm = topic.replace("™", "").strip()
        return (
            By.XPATH,
            f"//select[@id='helpTopic' or contains(@aria-label,'Help') or contains(@name,'topic')]"
            f"/option[contains(translate(normalize-space(.), '\u2122', ''), "
            f"'{topic_norm}')]",
        )

    def _link_by_keywords(self, keywords):
        xp_parts = " or ".join(
            [f"contains(translate(normalize-space(.), '\u2122', ''), '{k}')" for k in keywords]
        )
        return (By.XPATH, f"(//main//a[{xp_parts}] | //a[{xp_parts}])[1]")

    # ---------- Init ----------
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ---------- Navigation ----------
    def open_returns_page(self):
        self.driver.get(self.HELP_URL_RETURNS)
        self._wait_for_any_title()
        self.verify_returns_opened()

    # ---------- Actions ----------
    def select_help_topic(self, topic_text: str):
        """Attempt direct URL → dropdown → link → search fallback"""
        if self._try_direct_url(topic_text):
            self._post_select_waits(topic_text)
            return
        if self._try_select_dropdown(topic_text, 4):
            self._post_select_waits(topic_text)
            return
        if self._try_click_link(topic_text, 6):
            self._post_select_waits(topic_text)
            return
        self._search_and_open(topic_text)
        self._post_select_waits(topic_text)

    # ---------- Verifications ----------
    def verify_returns_opened(self):
        if not self._wait_url_or_title_contains_any(
            ["Returns", "Exchanges", "parentcat=Returns", "parentcat=Returns+%26+Exchanges"],
            20,
        ):
            raise SELex.TimeoutException("Returns page not detected via URL or title.")

    def verify_current_promotions_opened(self):
        self._must_url_or_title_contains_any(
            ["Promotions", "Coupons", "Current promotions", "Current+promotions"]
        )

    def verify_about_target_circle_opened(self):
        """
        Accept URL/title variants AND DOM evidence that we're on a Circle page.
        """
        fragments = [
            # URL variants
            "Target+Circle", "Target%20Circle", "target-circle", "/Target-Circle", "/circle",
            # Title/heading variants
            "About Target Circle", "Target Circle", "Target Circle™",
            "Circle benefits", "Target Circle terms", "Target Circle™ terms",
            "Target Circle rewards",
        ]
        if self._wait_url_or_title_contains_any(fragments, 25):
            return
        # DOM fallback: look for visible text mentioning 'circle'
        try:
            WebDriverWait(self.driver, 25).until(
                lambda d: len(d.find_elements(
                    By.XPATH,
                    "//*[self::h1 or self::h2 or self::h3]"
                    "[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'circle')]"
                    " | //nav[contains(@class,'breadcrumb') or @aria-label='breadcrumb']"
                    "//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'circle')]"
                    " | //main//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'target circle')]"
                )) > 0
            )
            return
        except SELex.TimeoutException:
            self._debug_where_am_i("verify_about_target_circle_opened")
            raise SELex.TimeoutException("Target Circle page not detected via URL/title/DOM.")

    # ---------- Internal helpers ----------
    def _keywords_for_topic(self, topic_text: str):
        t = topic_text.replace("™", "").strip()
        if "Promotion" in t or "Coupon" in t:
            return ["Current promotions", "Promotions", "Coupons"]
        if "Target Circle" in t:
            return [
                "About Target Circle", "Target Circle", "Target Circle™",
                "Circle benefits", "Target Circle terms", "Target Circle™ terms",
                "Target Circle rewards",
            ]
        return [t]

    def _try_select_dropdown(self, topic_text: str, short_timeout: int) -> bool:
        short_wait = WebDriverWait(self.driver, short_timeout)
        try:
            dropdown = short_wait.until(EC.presence_of_element_located(self._TOPIC_DROPDOWN))
            short_wait.until(EC.element_to_be_clickable(self._TOPIC_DROPDOWN))
            dropdown.click()
            option = short_wait.until(
                EC.presence_of_element_located(self._topic_option_by_text(topic_text))
            )
            option.click()
            return True
        except SELex.TimeoutException:
            return False

    def _try_click_link(self, topic_text: str, short_timeout: int) -> bool:
        short_wait = WebDriverWait(self.driver, short_timeout)
        try:
            link_locator = self._link_by_keywords(self._keywords_for_topic(topic_text))
            link = short_wait.until(EC.element_to_be_clickable(link_locator))
            self._safe_click(link)
            return True
        except SELex.TimeoutException:
            return False

    def _try_direct_url(self, topic_text: str) -> bool:
        key = topic_text.replace("™", "").strip()
        url = self.DIRECT_TOPIC_URLS.get(key)
        if url:
            self.driver.get(url)
            self._wait_for_any_title()
            return True
        return False

    def _search_and_open(self, topic_text: str):
        q = quote_plus(topic_text.replace("™", "").strip())
        self.driver.get(f"https://help.target.com/s/?q={q}")
        first_result = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//main//a[contains(@href,'help/')])[1]"))
        )
        self._safe_click(first_result)
        self._wait_for_any_title()

    def _post_select_waits(self, topic_text: str):
        keywords = self._keywords_for_topic(topic_text)
        if not self._wait_url_or_title_contains_any(keywords, 20):
            extras = [topic_text.replace("&", "%26"), topic_text.replace("™", "")]
            self._wait_url_or_title_contains_any(extras, 10)

    def _safe_click(self, el):
        try:
            el.click()
        except SELex.ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            self.driver.execute_script("arguments[0].click()", el)

    # ---------- Wait helpers ----------
    def _wait_for_any_title(self, timeout=20):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self._PAGE_TITLE))

    def _get_title_text(self) -> str:
        try:
            el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self._PAGE_TITLE))
            return el.text or ""
        except SELex.TimeoutException:
            return ""

    def _wait_url_or_title_contains_any(self, fragments, timeout=20) -> bool:
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(
                lambda d: any(frag and frag.lower() in d.current_url.lower() for frag in fragments)
                or any(frag and frag.lower() in self._get_title_text().lower() for frag in fragments)
            )
        except SELex.TimeoutException:
            return False

    def _must_url_or_title_contains_any(self, fragments, timeout=20):
        if not self._wait_url_or_title_contains_any(fragments, timeout):
            raise SELex.TimeoutException(f"Expected one of {fragments} in URL or title.")

    def _debug_where_am_i(self, note=""):
        try:
            title_text = self._get_title_text()
        except Exception:
            title_text = "<no title el>"
        print(f"[HELP DEBUG] {note} | URL={self.driver.current_url} | TITLE={title_text}")