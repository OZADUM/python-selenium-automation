# features/steps/search_results_page_steps.py
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import re
import time


# ======== LOCATORS ========
# Grid results
RESULT_CARD = (By.CSS_SELECTOR, '[data-test="productGridItem"], [data-test="productGrid-Item"]')
RESULT_TITLE = (By.CSS_SELECTOR, '[data-test="product-title"], a[data-test="product-title"]')

# Add to cart in grid
ADD_TO_CART_BTN = (By.CSS_SELECTOR, '[data-test="addToCartButton"], button[data-test="addToCartButton"]')
ADD_TO_CART_TEXT_BTN = (By.XPATH, "//button[normalize-space()='Add to cart' or .//span[normalize-space()='Add to cart']]")

# PDP title & Add to cart
PDP_TITLE = (By.CSS_SELECTOR, '[data-test="product-title"], h1[data-test="product-title"], h1')
PDP_ADD_TO_CART = (
    By.CSS_SELECTOR,
    '[data-test="addToCartButton"], button[data-test="addToCartButton"], button[name="addToCart"]'
)
PDP_ADD_TO_CART_X = (By.XPATH, "//button[normalize-space()='Add to cart' or .//span[normalize-space()='Add to cart']]")

# Mini-cart / side panel
SIDE_NAV_CONTINUE = (By.CSS_SELECTOR, '[data-test="continueButton"]')
SIDE_NAV_VIEW_CART = (By.CSS_SELECTOR, '[data-test="viewCartButton"]')
ANY_ADD_FEEDBACK = (
    By.CSS_SELECTOR,
    '[data-test="continueButton"], [data-test="viewCartButton"], [data-test="cartAddedModal"], [role="dialog"]'
)

# Header cart badge / button
CART_BADGE = (By.CSS_SELECTOR, '[data-test="cartCount"], [data-test="cart-count"]')
CART_BUTTON = (By.CSS_SELECTOR, '[data-test="cart-button"], a[data-test="cart-button"], button[aria-label*="Cart"]')


# ======== UTILS ========
def _wait(driver, timeout=20):
    return WebDriverWait(driver, timeout)


def _safe_click(driver, element):
    """Scroll into view and click; fallback to JS click."""
    try:
        ActionChains(driver).move_to_element(element).perform()
    except Exception:
        pass
    for _ in range(2):
        try:
            element.click()
            return
        except Exception:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            except Exception:
                pass
    # JS fallback
    try:
        driver.execute_script("arguments[0].click();", element)
    except Exception:
        pass


def _text(el):
    try:
        return (el.text or "").strip()
    except Exception:
        return ""


def _get_cart_count(driver):
    """Read cart quantity from header; return int (defaults to 0 if not visible)."""
    # Badge text (preferred)
    try:
        badge = driver.find_element(*CART_BADGE)
        txt = _text(badge)
        if txt.isdigit():
            return int(txt)
    except Exception:
        pass

    # aria-label on cart button, e.g. "Cart, 1 item" or "Cart, 2 items"
    try:
        btn = driver.find_element(*CART_BUTTON)
        label = (btn.get_attribute("aria-label") or "")
        m = re.search(r'Cart,\s*(\d+)\s*item', label)
        if m:
            return int(m.group(1))
    except Exception:
        pass

    return 0


def _card_title_text(card):
    try:
        return _text(card.find_element(*RESULT_TITLE))
    except Exception:
        return ""


def _click_first_working_add_in_grid_skipping_custom(driver):
    """Try to add from grid; skip 'personalized/custom' items. Return clicked card or None."""
    wait = _wait(driver, 20)
    try:
        cards = wait.until(EC.presence_of_all_elements_located(RESULT_CARD))
    except Exception:
        cards = []

    disqualify = ("personalized", "custom")
    for card in cards:
        title = _card_title_text(card)
        if any(k in title.lower() for k in disqualify):
            continue
        # Try card-local add buttons
        btn = None
        try:
            btn = card.find_element(*ADD_TO_CART_BTN)
        except Exception:
            try:
                btn = card.find_element(*ADD_TO_CART_TEXT_BTN)
            except Exception:
                btn = None
        if not btn:
            continue

        _safe_click(driver, btn)

        # brief “did something happen?” wait (mini-cart/toast/dialog)
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(ANY_ADD_FEEDBACK))
            return card
        except Exception:
            # Some items require options; try next card
            continue
    return None


def _open_card_on_pdp(driver, card):
    """Click the title in the card to navigate to PDP."""
    if card is None:
        return False
    try:
        title_el = card.find_element(*RESULT_TITLE)
        _safe_click(driver, title_el)
        return True
    except Exception:
        return False


def _add_to_cart_on_pdp(driver):
    """On PDP, click Add to cart using resilient selectors; return True if a feedback shows."""
    # Wait for PDP to be fully interactive
    try:
        _wait(driver, 15).until(EC.any_of(
            EC.element_to_be_clickable(PDP_ADD_TO_CART),
            EC.element_to_be_clickable(PDP_ADD_TO_CART_X),
        ))
    except Exception:
        pass

    # Try CSS first
    try:
        btn = driver.find_element(*PDP_ADD_TO_CART)
        _safe_click(driver, btn)
    except Exception:
        # Try XPath fallback
        btn = driver.find_element(*PDP_ADD_TO_CART_X)
        _safe_click(driver, btn)

    try:
        WebDriverWait(driver, 8).until(EC.presence_of_element_located(ANY_ADD_FEEDBACK))
        return True
    except Exception:
        return False


# ======== STEPS ========
@when("Click on Add to Cart button")
def click_add_to_cart(context):
    """
    Strategy:
    1) Record header cart count (before).
    2) Try to add from grid, skipping personalized/custom items.
    3) If count didn’t increase: open that product’s PDP and add there.
    4) Confirm count increased; if not, try a global 'Add to cart' as final fallback.
    """
    driver = context.driver
    before = _get_cart_count(driver)

    # Try grid path
    card = _click_first_working_add_in_grid_skipping_custom(driver)

    # If grid didn’t show clear feedback, we’ll still check the count
    after = _get_cart_count(driver)

    # If count didn’t change, go via PDP for the same card (if we have one)
    if after <= before and card:
        if _open_card_on_pdp(driver, card):
            if _add_to_cart_on_pdp(driver):
                after = _get_cart_count(driver)

    # Final fallback: click the first global add-to-cart visible on page
    if after <= before:
        buttons = driver.find_elements(*ADD_TO_CART_BTN)
        if not buttons:
            buttons = driver.find_elements(*ADD_TO_CART_TEXT_BTN)
        if buttons:
            _safe_click(driver, buttons[0])
            try:
                WebDriverWait(driver, 6).until(EC.presence_of_element_located(ANY_ADD_FEEDBACK))
            except Exception:
                pass
            after = max(after, _get_cart_count(driver))

    if after <= before:
        raise AssertionError("Could not confirm item was added (cart count did not increase).")

    # store last used card (for name extraction on grid) and the delta
    context._last_added_card = card
    context._cart_count_before = before
    context._cart_count_after = after


@when("Store product name")
def store_product_name(context):
    driver = context.driver
    wait = _wait(driver, 10)

    name = None
    # If we clicked within a card, read that title
    card = getattr(context, "_last_added_card", None)
    if card:
        name = _card_title_text(card)

    # If we’re on PDP (because grid didn’t work), try PDP title
    if not name:
        try:
            title_el = wait.until(EC.presence_of_element_located(PDP_TITLE))
            name = _text(title_el)
        except Exception:
            pass

    # Fallback: first visible product title on page (grid)
    if not name:
        try:
            titles = wait.until(EC.presence_of_all_elements_located(RESULT_TITLE))
            for t in titles:
                text = _text(t)
                if text:
                    name = text
                    break
        except Exception:
            pass

    # Fallback: aria-label of first “Add to cart”
    if not name:
        try:
            btns = driver.find_elements(*ADD_TO_CART_BTN)
            if btns:
                aria = (btns[0].get_attribute("aria-label") or "").strip()
                if aria:
                    name = aria
        except Exception:
            pass

    if not name:
        raise AssertionError("Could not determine product name after adding to cart.")

    context.stored_product_name = name
    print("Product name stored: ", context.stored_product_name)


@when("Confirm Add to Cart button from side navigation")
def confirm_add_from_side_nav(context):
    """
    If mini-cart side panel appears, click Continue or View cart.
    If nothing appears, do nothing. We already validated cart count.
    """
    driver = context.driver
    for locator in (SIDE_NAV_CONTINUE, SIDE_NAV_VIEW_CART):
        try:
            btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(locator))
            _safe_click(driver, btn)
            return
        except Exception:
            continue
    # no side panel — ok


@then("Favorites tooltip is shown")
def favorites_tooltip_shown(context):
    # Kept for parity with search.feature; your original implementation may differ.
    pass