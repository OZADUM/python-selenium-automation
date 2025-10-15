# pages/sign_in_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    InvalidElementStateException,
    ElementNotInteractableException,
)
from selenium.webdriver.common.keys import Keys
from pages.base_page import Page


class SignInPage(Page):
    ACCOUNT_URL = "https://www.target.com/account"
    FALLBACK_LOGIN_URL = "https://www.target.com/login"

    # --- Common banners / buttons ---
    COOKIE_ACCEPT_BTNS = [
        (By.ID, "onetrust-accept-btn-handler"),
        (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),
        (By.XPATH, "//button[contains(., 'Accept') and contains(., 'Cookies')]"),
    ]

    ACCOUNT_SIGNIN_BTNS = [
        (By.CSS_SELECTOR, "[data-test='accountNav-signIn']"),
        (By.XPATH, "//a[normalize-space()='Sign in']"),
        (By.XPATH, "//button[normalize-space()='Sign in']"),
        (By.XPATH, "//span[normalize-space()='Sign in']/ancestor::a|//span[normalize-space()='Sign in']/ancestor::button"),
    ]

    # --- Iframe candidates for embedded auth modal ---
    IFRAME_CANDIDATES = [
        (By.CSS_SELECTOR, "iframe[src*='login']"),
        (By.CSS_SELECTOR, "iframe[src*='account']"),
        (By.CSS_SELECTOR, "iframe[id*='login']"),
        (By.CSS_SELECTOR, "iframe[name*='login']"),
        (By.TAG_NAME, "iframe"),
    ]

    # --- Email / Continue ---
    EMAIL_INPUTS = [
        (By.ID, "username"),
        (By.CSS_SELECTOR, "input#username"),
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "input[type='email']"),
    ]
    CONTINUE_BTNS = [
        (By.ID, "login"),
        (By.CSS_SELECTOR, "button#login"),
        (By.XPATH, "//button[.//span[normalize-space()='Continue'] or normalize-space()='Continue']"),
        (By.XPATH, "//button[contains(., 'Continue')]"),
    ]

    # --- Password-mode toggles (very loose text to catch variants) ---
    PASSWORD_TOGGLE_BTNS = [
        (By.XPATH, "//*[self::a or self::button][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'use password')]"),
        (By.XPATH, "//*[self::a or self::button][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in with password')]"),
        (By.XPATH, "//*[self::a or self::button][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enter password')]"),
        (By.XPATH, "//*[self::a or self::button][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'password')]"),
        (By.XPATH, "//*[self::a or self::button][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'try another way')]"),
        (By.XPATH, "//*[self::a or self::button][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'use a different method')]"),
    ]

    # --- Password / submit ---
    PASSWORD_INPUTS = [
        (By.ID, "password"),
        (By.CSS_SELECTOR, "input#password"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "input[autocomplete='current-password']"),
        (By.CSS_SELECTOR, "input[aria-label*='password' i]"),
    ]

    # Broad submit button locators + fallbacks
    SUBMIT_BTNS = [
        (By.XPATH, "//button[.//span[contains(., 'Sign in with password')] or contains(., 'Sign in with password')]"),
        (By.XPATH, "//button[contains(., 'Sign in') and contains(., 'password')]"),
        (By.XPATH, "//button[.//span[normalize-space()='Sign in'] or normalize-space()='Sign in']"),
        (By.ID, "login"),
        (By.CSS_SELECTOR, "button#login"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, "[data-test*='sign' i]"),
        (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign in')]"),
        (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'log in')]"),
    ]

    ERROR_BANNERS = [
        (By.CSS_SELECTOR, "[data-test='authAlertError']"),
        (By.CSS_SELECTOR, "[role='alert']"),
        (By.XPATH, "//*[contains(@class,'Alert') or contains(@class,'error')][.//text()]"),
    ]

    # ---------- helpers ----------
    def _click_if_present(self, locators, timeout=2) -> bool:
        for by, sel in locators:
            try:
                el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, sel)))
                el.click()
                return True
            except TimeoutException:
                continue
        return False

    def _first_present(self, locators, timeout=10):
        last_exc = None
        for by, sel in locators:
            try:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, sel)))
            except TimeoutException as e:
                last_exc = e
        raise NoSuchElementException(f"None of the locators were found: {locators}") from last_exc

    def _first_clickable(self, locators, timeout=10):
        last_exc = None
        for by, sel in locators:
            try:
                return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, sel)))
            except TimeoutException as e:
                last_exc = e
        raise NoSuchElementException(f"None of the locators became clickable: {locators}") from last_exc

    def _accept_cookies_if_shown(self):
        self._click_if_present(self.COOKIE_ACCEPT_BTNS, timeout=2)

    def _switch_into_iframe_containing(self, locators) -> bool:
        # Try current context first
        try:
            self._first_present(locators, timeout=2)
            return True
        except Exception:
            pass

        # Scan frames
        frames = []
        for by, sel in self.IFRAME_CANDIDATES:
            frames = self.driver.find_elements(by, sel)
            if frames:
                break

        for fr in frames:
            self.driver.switch_to.default_content()
            try:
                self.driver.switch_to.frame(fr)
                self._first_present(locators, timeout=2)
                return True
            except Exception:
                continue

        self.driver.switch_to.default_content()
        return False

    def _reenter_iframe_if_needed_for_password(self) -> None:
        """After Continue, UI may rebuild; find password either in current context or in another iframe."""
        try:
            self._first_present(self.PASSWORD_INPUTS, timeout=3)
            return
        except Exception:
            pass

        # Try clicking a password-mode toggle if present
        self._click_if_present(self.PASSWORD_TOGGLE_BTNS, timeout=3)

        # Try current context again
        try:
            self._first_present(self.PASSWORD_INPUTS, timeout=3)
            return
        except Exception:
            pass

        # Re-scan iframes for password field
        self.driver.switch_to.default_content()
        self._switch_into_iframe_containing(self.PASSWORD_INPUTS)

    # ---------- public API ----------
    def open(self):
        self.driver.get(self.ACCOUNT_URL)
        self._accept_cookies_if_shown()
        self._click_if_present(self.ACCOUNT_SIGNIN_BTNS, timeout=4)

        if not self._switch_into_iframe_containing(self.EMAIL_INPUTS):
            self.driver.get(self.FALLBACK_LOGIN_URL)
            self._accept_cookies_if_shown()
            self._switch_into_iframe_containing(self.EMAIL_INPUTS)

        self._first_present(self.EMAIL_INPUTS, timeout=10)

    def enter_email_and_continue(self, email: str):
        email_el = self._first_present(self.EMAIL_INPUTS, timeout=10)
        try:
            email_el.clear()
        except (InvalidElementStateException, ElementNotInteractableException):
            self.driver.execute_script("arguments[0].value = '';", email_el)
        email_el.send_keys(email)
        btn = self._first_clickable(self.CONTINUE_BTNS, timeout=10)
        btn.click()

    def enter_password_and_submit(self, password: str):
        # Ensure we are on the password screen and in the correct iframe
        self._reenter_iframe_if_needed_for_password()

        # Try a clickable password input first
        try:
            pw = self._first_clickable(self.PASSWORD_INPUTS, timeout=10)
        except NoSuchElementException:
            pw = self._first_present(self.PASSWORD_INPUTS, timeout=10)

        # Scroll and clear robustly
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pw)
        except Exception:
            pass
        try:
            pw.clear()
        except (InvalidElementStateException, ElementNotInteractableException):
            self.driver.execute_script("arguments[0].value = '';", pw)

        # Type password (fallback JS)
        try:
            pw.send_keys(password)
        except (InvalidElementStateException, ElementNotInteractableException):
            self.driver.execute_script("arguments[0].value = arguments[1];", pw, password)

        # ---- Submit sequence with fallbacks ----
        # 1) Normal clickable button
        try:
            submit = self._first_clickable(self.SUBMIT_BTNS, timeout=6)
            submit.click()
            return
        except Exception:
            pass

        # 2) Press ENTER in the password field
        try:
            pw.send_keys(Keys.RETURN)
            return
        except Exception:
            pass

        # 3) JS click on any generic submit/button we can find
        try:
            self.driver.execute_script("""
                const btn = document.querySelector('button[type=submit],input[type=submit],button#login,[data-test*=sign i]');
                if (btn) btn.click();
            """)
            return
        except Exception:
            pass

        # 4) Last resort: raise a clear error
        raise NoSuchElementException("Could not find/click a Sign In submit button after entering password.")

    def error_is_visible(self) -> str:
        try:
            el = self._first_present(self.ERROR_BANNERS, timeout=10)
            return (el.text or "").strip()
        except Exception:
            return ""

    # ---------- Post-submit status helpers ----------
    def _text_present(self, needle_lower: str) -> bool:
        try:
            body = self.driver.find_element(By.TAG_NAME, "body").text or ""
            return needle_lower in body.lower()
        except Exception:
            return False

    def password_field_visible(self) -> bool:
        try:
            self._first_present(self.PASSWORD_INPUTS, timeout=3)
            return True
        except Exception:
            return False

    def inline_password_error(self) -> str:
        """Try common inline error patterns near the password input."""
        candidates = [
            (By.CSS_SELECTOR, "[id*='error' i]"),
            (By.CSS_SELECTOR, "[data-test*='error' i]"),
            (By.CSS_SELECTOR, "[aria-live='assertive']"),
            (By.XPATH, "//input[@type='password']/following::*[self::div or self::p][contains(@class,'error') or contains(@class,'Error')][1]"),
        ]
        for by, sel in candidates:
            try:
                el = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((by, sel)))
                txt = (el.text or "").strip()
                if txt:
                    return txt
            except TimeoutException:
                continue
        return ""

    def challenge_visible(self) -> bool:
        """Heuristic: look for typical words shown on verification / code pages."""
        needles = [
            "verify", "verification", "security code", "enter code",
            "we sent a code", "two-step", "2-step", "multifactor",
        ]
        return any(self._text_present(n) for n in needles)

    def auth_failed_or_challenged(self):
        """
        Returns (ok, evidence): ok=True if we see banner error, inline error,
        a challenge screen, or we are still on a password page (not logged in).
        """
        banner = self.error_is_visible()
        if banner:
            return True, f"banner: {banner}"

        inline = self.inline_password_error()
        if inline:
            return True, f"inline: {inline}"

        if self.challenge_visible():
            return True, "challenge screen detected"

        if self.password_field_visible():
            return True, "still on password screen (not logged in)"

        return False, "no error/challenge detected"