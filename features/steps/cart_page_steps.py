from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CART_URL = "https://www.target.com/cart"

# --- Common cart markers (Target DOM can vary) ---
CART_CONTENT = (By.CSS_SELECTOR, "[data-test='cartContent']")
CART_EMPTY_MSG = (By.CSS_SELECTOR, "[data-test='boxEmptyMsg']")
CART_ITEM = (By.CSS_SELECTOR, "[data-test='cartItem']")
PRODUCT_TITLE = (By.CSS_SELECTOR, "[data-test='cartItem'] [data-test='cartItem-title']")

# A few alternative/legacy hooks (kept loose on purpose)
CART_ROOT_FALLBACKS = [
    (By.CSS_SELECTOR, "#cart-root"),
    (By.CSS_SELECTOR, "[data-test='cart']"),
    (By.CSS_SELECTOR, "[data-test='cartItems']"),
]


def _wait(context, timeout=15):
    return context.driver.wait if hasattr(context.driver, "wait") else WebDriverWait(context.driver, timeout)


def _any_present(driver, locators):
    for by, sel in locators:
        els = driver.find_elements(by, sel)
        if els:
            return True
    return False


def _wait_for_cart_loaded(context, allow_refresh=True):
    w = _wait(context, 15)

    # 1) Ensure we're on /cart
    w.until(lambda d: "/cart" in d.current_url.lower())

    # 2) Accept any of these as "cart loaded"
    primary_markers = [CART_CONTENT, CART_EMPTY_MSG, CART_ITEM, PRODUCT_TITLE]
    fallback_markers = CART_ROOT_FALLBACKS

    def cart_ready(d):
        return _any_present(d, primary_markers) or _any_present(d, fallback_markers)

    try:
        w.until(cart_ready)
    except Exception:
        if allow_refresh:
            # One-time refresh fallback (Target can be slow to hydrate the cart)
            context.driver.refresh()
            w.until(lambda d: "/cart" in d.current_url.lower())
            w.until(cart_ready)
        else:
            raise


@when("Open cart page")
def open_cart(context):
    # Navigate directly to cart; side drawer from PDP shouldn't block a hard navigation
    context.driver.get(CART_URL)
    _wait_for_cart_loaded(context, allow_refresh=True)


@then("Verify 'Your cart is empty' message is shown")
def verify_cart_empty_message(context):
    w = _wait(context, 15)
    # Either the explicit empty box or (rarely) a message container in the cart root
    w.until(EC.presence_of_element_located(CART_EMPTY_MSG))
    assert context.driver.find_element(*CART_EMPTY_MSG).is_displayed(), "Empty cart message is not visible"


@then("Verify cart has {qty:d} item(s)")
def verify_cart_has_qty(context, qty):
    _wait_for_cart_loaded(context, allow_refresh=False)

    # Give the DOM a brief chance to hydrate the line items
    w = _wait(context, 10)
    def count_items(d):
        return len(d.find_elements(*CART_ITEM))

    # If we expect >0, wait until at least one appears (up to timeout)
    if qty > 0:
        try:
            w.until(lambda d: count_items(d) >= 1)
        except Exception:
            pass  # fall through to final count check

    actual = len(context.driver.find_elements(*CART_ITEM))
    assert actual == qty, f"Expected {qty} items but got {actual}"


@then("Verify cart has correct product")
def verify_cart_product(context):
    """
    Requires context.product_name to be set earlier (e.g., from side drawer):
        context.product_name = driver.find_element(...).text
    """
    expected = (getattr(context, "product_name", "") or "").strip()
    assert expected, "No product name stored in context.product_name"

    _wait_for_cart_loaded(context, allow_refresh=False)

    w = _wait(context, 10)
    w.until(EC.presence_of_all_elements_located(CART_ITEM))  # ensure at least one line item is present

    titles = [el.text.strip() for el in context.driver.find_elements(*PRODUCT_TITLE)]
    found = any(expected.lower() in t.lower() for t in titles)

    assert found, f"Expected product '{expected}' not found in cart titles: {titles}"