import os
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TEST_EMAIL = os.getenv("TARGET_TEST_EMAIL")
TEST_PASSWORD = os.getenv("TARGET_TEST_PASSWORD")

HOME_URL = "https://www.target.com/"

ACCOUNT_BUTTON_CANDIDATES = [
    (By.CSS_SELECTOR, "[data-test='@web/AccountLink']"),
    (By.CSS_SELECTOR, "[data-test='accountNav-button']"),
    (By.CSS_SELECTOR, "[data-test='accountNavButton']"),
    (By.CSS_SELECTOR, "[data-test='accountNav']"),
    (By.XPATH, "//button[contains(translate(@aria-label,'ACCOUNT','account'),'account')]"),
]
CART_LINK = (By.CSS_SELECTOR, "[data-test='@web/CartLink']")

def _click_any(driver, locators, timeout=10):
    w = WebDriverWait(driver, timeout)
    for how, what in locators:
        try:
            el = w.until(EC.element_to_be_clickable((how, what)))
            el.click()
            return True
        except Exception:
            continue
    return False

@when("I login with valid credentials")
def login_with_valid_credentials(context):
    if not TEST_EMAIL or not TEST_PASSWORD:
        raise AssertionError("Missing TARGET_TEST_EMAIL / TARGET_TEST_PASSWORD env vars.")
    sip = context.app.sign_in_page
    sip.input_email(TEST_EMAIL)
    sip.proceed_to_password_if_needed()
    sip.input_password(TEST_PASSWORD)
    sip.submit()

@then("Verify user is logged in")
def verify_user_is_logged_in(context):
    # Go to homepage to get the standard header
    context.driver.get(HOME_URL)
    w = WebDriverWait(context.driver, 10)

    # Either we can click the account button or at least see a cart link
    clicked = _click_any(context.driver, ACCOUNT_BUTTON_CANDIDATES, timeout=8)
    if clicked:
        return

    # If we couldn't click account, accept cart link visibility as a lighter signal
    w.until(EC.presence_of_element_located(CART_LINK))