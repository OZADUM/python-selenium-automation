from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

class SignInPage:
    EMAIL = (By.CSS_SELECTOR, "#username, input[name='username'], input[type='email']")
    PASSWORD = (By.CSS_SELECTOR, "#password, input[name='password'], input[type='password']")

    # Try these in order
    SUBMIT_CANDIDATES = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "[data-test='login']"),
        (By.CSS_SELECTOR, "[data-test='accountForm-submit'], [data-test='accountForm-submitButton']"),
        (By.CSS_SELECTOR, "[data-test='continue']"),
        (By.XPATH, "//button[.//span[normalize-space()='Sign in'] or normalize-space()='Sign in']"),
        (By.XPATH, "//button[.//span[normalize-space()='Continue'] or normalize-space()='Continue']"),
    ]

    HEADING = (By.XPATH,
               "//h1[contains(.,'Sign in') or contains(.,'Sign In')] | "
               "//h2[contains(.,'Sign in') or contains(.,'Sign In')]")

    # Header signals post-login
    POST_LOGIN_SIGNALS = [
        (By.CSS_SELECTOR, "[data-test='@web/AccountLink'], [data-test='accountNav-button'], [data-test='accountNavButton']"),
        (By.CSS_SELECTOR, "[data-test='@web/CartLink']"),
    ]

    def __init__(self, driver, timeout: int = 12):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- utils ---
    def _wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _is_present(self, locator) -> bool:
        return len(self.driver.find_elements(*locator)) > 0

    def _click_any(self, locators, timeout=8) -> bool:
        w = WebDriverWait(self.driver, timeout)
        for how, what in locators:
            try:
                el = w.until(EC.element_to_be_clickable((how, what)))
                el.click()
                return True
            except Exception:
                continue
        return False

    # --- flow ---
    def verify_opened(self):
        if "/login" in self.driver.current_url.lower():
            try:
                self.wait.until(lambda d: d.find_elements(*self.EMAIL)
                                       or d.find_elements(*self.PASSWORD)
                                       or d.find_elements(*self.HEADING))
            except TimeoutException:
                pass
            return
        self.wait.until(lambda d: d.find_elements(*self.EMAIL)
                               or d.find_elements(*self.PASSWORD)
                               or d.find_elements(*self.HEADING))

    def input_email(self, email: str):
        el = self._wait_visible(self.EMAIL)
        try:
            el.clear()
        except Exception:
            pass
        el.click()
        el.send_keys(email)

    def proceed_to_password_if_needed(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.PASSWORD))
            return
        except TimeoutException:
            pass
        self._click_any(self.SUBMIT_CANDIDATES, timeout=4)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.PASSWORD))

    def input_password(self, password: str):
        last_err = None
        for _ in range(3):
            try:
                el = self.wait.until(EC.element_to_be_clickable(self.PASSWORD))
                try:
                    el.clear()
                except Exception:
                    pass
                el.click()
                el.send_keys(password)
                return
            except (StaleElementReferenceException, TimeoutException) as e:
                last_err = e
        raise last_err or Exception("Unable to type into password field after retries.")

    def submit(self):
        clicked = self._click_any(self.SUBMIT_CANDIDATES, timeout=6)
        if not clicked:
            try:
                el = self.wait.until(EC.element_to_be_clickable(self.PASSWORD))
                el.send_keys(Keys.ENTER)
            except TimeoutException:
                el = self._wait_visible(self.EMAIL)
                el.send_keys(Keys.ENTER)

        # short post-submit: URL away from /login OR header signal
        short_wait = WebDriverWait(self.driver, 6)
        try:
            short_wait.until(lambda d: "/login" not in d.current_url.lower())
            return
        except TimeoutException:
            for how, what in self.POST_LOGIN_SIGNALS:
                try:
                    short_wait.until(EC.presence_of_element_located((how, what)))
                    return
                except TimeoutException:
                    continue
        # let the step decide next