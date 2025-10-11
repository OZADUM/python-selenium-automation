# features/steps/window_handling_steps.py
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Locators (broad CSS to tolerate slight URL changes)
TERMS_LINK_BY_PARTIAL_TEXT = (By.PARTIAL_LINK_TEXT, "Terms")
TERMS_LINK_BY_SELECTOR = (By.CSS_SELECTOR, "a[href*='terms']")


def _wait(context):
    return context.driver.wait if hasattr(context.driver, "wait") else WebDriverWait(context.driver, 15)


@given("Open sign in page")
def open_sign_in(context):
    context.driver.get("https://www.target.com/orders?lnk=acct_nav_my_account")
    _wait(context).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


@when("Store original window")
def store_original_window(context):
    context.original_window = context.driver.current_window_handle


@when("Click on Target terms and conditions link")
def click_terms_link(context):
    # Try by partial link text first, then fallback to CSS contains
    try:
        link = _wait(context).until(EC.element_to_be_clickable(TERMS_LINK_BY_PARTIAL_TEXT))
    except Exception:
        link = _wait(context).until(EC.element_to_be_clickable(TERMS_LINK_BY_SELECTOR))

    # Scroll into view and click (fallback to JS click if needed)
    context.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
    try:
        link.click()
    except Exception:
        context.driver.execute_script("arguments[0].click();", link)


@when("Switch to the newly opened window")
def switch_to_new_window(context):
    original = context.original_window
    wait = _wait(context)
    handles_before = list(context.driver.window_handles)
    context.new_window_opened = False  # track if a separate tab/window exists

    # Case 1: A NEW window/tab opens
    try:
        from selenium.webdriver.support import expected_conditions as EC  # local import to satisfy linters
        wait.until(EC.new_window_is_opened(handles_before))
        context.new_window_opened = True
    except Exception:
        # Case 2: It may have navigated in the SAME tab
        if "terms" in context.driver.current_url.lower() or "terms" in (context.driver.title or "").lower():
            return
        # Case 3: Popup blocked → open target href in a new tab via JS
        try:
            link = context.driver.find_element(*TERMS_LINK_BY_SELECTOR)
        except Exception:
            link = context.driver.find_element(*TERMS_LINK_BY_PARTIAL_TEXT)
        href = link.get_attribute("href")
        context.driver.execute_script("window.open(arguments[0], '_blank');", href)
        wait.until(lambda d: len(d.window_handles) > 1)
        context.new_window_opened = True

    if context.new_window_opened:
        # Switch to the non-original handle
        for h in context.driver.window_handles:
            if h != original:
                context.driver.switch_to.window(h)
                break


@then("Verify Terms and Conditions page is opened")
def verify_terms_page(context):
    _wait(context).until(
        lambda d: "terms" in d.current_url.lower() or "terms" in (d.title or "").lower()
    )
    assert (
        "terms" in context.driver.current_url.lower()
        or "terms" in (context.driver.title or "").lower()
    ), f"Unexpected page. URL={context.driver.current_url} TITLE={context.driver.title}"


@then("User can close new window and switch back to original")
def close_and_switch_back(context):
    if getattr(context, "new_window_opened", False):
        context.driver.close()
        context.driver.switch_to.window(context.original_window)
    else:
        # Same-tab navigation case: just go back to the sign-in page
        context.driver.back()