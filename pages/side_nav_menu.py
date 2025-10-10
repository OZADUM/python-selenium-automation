from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SideNavMenu:
    """
    Handles whatever appears after clicking header "Sign in":
    - dropdown, dialog/sheet, or nothing (fallback to /login)
    """

    # Possible containers (we will "OR" them)
    SHEET_ROOTS = [
        (By.CSS_SELECTOR, "[data-test='accountNav']"),
        (By.CSS_SELECTOR, "[data-test='accountMenu']"),
        (By.CSS_SELECTOR, "[role='dialog']"),
        (By.XPATH, "//*[contains(@class,'Account') and contains(@class,'Nav')]"),
    ]

    # Any clickable Sign in menu entry/link/button
    SIGN_IN_CANDIDATES = [
        (By.CSS_SELECTOR, "[data-test='accountNav-signIn']"),
        (By.CSS_SELECTOR, "[data-test='accountMenu-signIn']"),
        (By.XPATH, "//a[contains(@href,'/login')]"),
        (By.XPATH, "//a[normalize-space()='Sign in' or normalize-space()='Sign In']"),
        (By.XPATH, "//button[normalize-space()='Sign in' or normalize-space()='Sign In']"),
    ]

    def __init__(self, driver, timeout: int = 8):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _try_wait_any(self, locators, condition):
        """Return the first element found by condition(locator) within the wait, else None."""
        for how, what in locators:
            try:
                return self.wait.until(condition((how, what)))
            except TimeoutException:
                continue
        return None

    def try_click_sign_in(self) -> bool:
        """
        Try to click Sign in entry from any menu/dropdown that appears.
        Returns True if something was clicked, False otherwise.
        """
        # Best-effort: wait briefly for any container to appear (dropdown or dialog)
        self._try_wait_any(self.SHEET_ROOTS, EC.visibility_of_element_located)

        # Now search for any sign-in candidate and click it
        for how, what in self.SIGN_IN_CANDIDATES:
            try:
                el = self.wait.until(EC.element_to_be_clickable((how, what)))
                el.click()
                return True
            except TimeoutException:
                continue
            except NoSuchElementException:
                continue
        return False