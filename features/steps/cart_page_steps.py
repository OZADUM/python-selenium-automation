# features/steps/cart_page_steps.py
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CART_URL = "https://www.target.com/cart"

EMPTY_MSG = (By.XPATH, "//*[contains(., \"Your cart is empty\")]")
ITEM_COUNT_BADGE = (By.CSS_SELECTOR, '[data-test="itemCount"], [data-test="cartSummaryItemCount"]')
CART_ITEM_TITLES = (By.CSS_SELECTOR, '[data-test="cartItem-title"], [data-test="product-title"]')


def _wait(driver, timeout=15):
    return WebDriverWait(driver, timeout)


@when("Open cart page")
def open_cart_page(context):
    context.driver.get(CART_URL)
    # wait for either empty message or cart content to load
    wait = _wait(context.driver)
    try:
        wait.until(
            EC.any_of(
                EC.presence_of_element_located(EMPTY_MSG),
                EC.presence_of_element_located(CART_ITEM_TITLES),
            )
        )
    except Exception:
        # not strictly fatal; let following steps assert specifics
        pass


@then("Verify 'Your cart is empty' message is shown")
def verify_cart_empty_message(context):
    _wait(context.driver).until(EC.visibility_of_element_located(EMPTY_MSG))


@then("Verify cart has {expected:d} item(s)")
def verify_cart_count(context, expected):
    """
    Be tolerant: either use an item count badge, or count visible cart item titles.
    """
    wait = _wait(context.driver)
    count = None

    # First try a numeric badge
    try:
        badge = wait.until(EC.presence_of_element_located(ITEM_COUNT_BADGE))
        txt = (badge.text or "").strip()
        if txt.isdigit():
            count = int(txt)
    except Exception:
        pass

    # Fallback: count the titles
    if count is None:
        try:
            titles = wait.until(EC.presence_of_all_elements_located(CART_ITEM_TITLES))
            count = len([t for t in titles if (t.text or "").strip()])
        except Exception:
            count = 0

    assert count == expected, f"Expected {expected} item(s) in cart, got {count}."


@then("Verify cart has correct product")
def verify_cart_has_correct_product(context):
    """
    Compare the stored product name (from search results) with the titles in the cart.
    Use a forgiving contains/substring match to account for slight differences.
    """
    expected_name = getattr(context, "stored_product_name", None) or getattr(context, "product_name", None)
    assert expected_name, (
        "No stored product name found (context.stored_product_name). "
        "Make sure you ran the 'Store product name' step before this assertion."
    )

    wait = _wait(context.driver)
    titles = wait.until(EC.presence_of_all_elements_located(CART_ITEM_TITLES))
    title_texts = [t.text.strip() for t in titles if (t.text or "").strip()]

    # relaxed matching: exact, contains, or case-insensitive contains
    exp = expected_name.strip()
    exp_low = exp.lower()

    match = any(
        (exp == title) or (exp in title) or (exp_low in title.lower())
        for title in title_texts
    )

    assert match, (
        f"Expected product '{expected_name}' not found in cart titles: {title_texts}"
    )