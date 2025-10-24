# features/steps/signin_invalid_steps.py
import os
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SIGNIN_URL = "https://www.target.com/account/sign-in"


def _get_test_email(context) -> str:
    # Priority: behave -D email="you@domain.com"
    email = context.config.userdata.get("email", "")
    if not email:
        email = os.environ.get("TARGET_TEST_EMAIL", "")
    return email.strip()


@given("I open Target Sign In page")
def open_signin(context):
    context.driver.get(SIGNIN_URL)
    WebDriverWait(context.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"], input[name="username"]'))
    )


@when('I enter email "__FROM_ENV__" and continue')
def enter_email_from_env(context):
    email = _get_test_email(context)
    print(f"[DEBUG] Using email: '{email}'")
    assert email, (
        "❌ No real email provided. Supply one of:\n"
        "  • behave:  -D email=\"you@domain.com\"\n"
        "  • env var: export TARGET_TEST_EMAIL=\"you@domain.com\"\n"
        "  • or hardcode locally in the feature."
    )

    driver = context.driver
    wait = WebDriverWait(driver, 10)
    email_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"], input[name="username"]')))
    email_box.clear()
    email_box.send_keys(email)

    # Continue/Next button
    next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"], button[data-test*="login"]')))
    next_btn.click()


@when('I enter password "{password}" and submit with password')
def enter_password(context, password: str):
    driver = context.driver
    wait = WebDriverWait(driver, 15)
    pwd_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"], input[name="password"]')))
    pwd_box.clear()
    pwd_box.send_keys(password)

    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"], button[data-test*="login"]')))
    submit.click()


@then("I see a sign-in error message")
def see_error(context):
    driver = context.driver
    wait = WebDriverWait(driver, 15)

    # Common places for auth errors
    error_selectors = [
        '[data-test*="error"], [id*="error"], [class*="error"]',
        '[role="alert"]',
        'div:has(svg[aria-label="error"]), div[aria-live="assertive"]',
    ]

    for sel in error_selectors:
        try:
            el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, sel)))
            msg = (el.text or "").strip()
            if msg:
                print(f"[DEBUG] Error shown: {msg}")
                return
        except Exception:
            continue

    # If we got here, nothing obvious was visible; still fail
    assert False, "Expected a sign-in error message, but none became visible."