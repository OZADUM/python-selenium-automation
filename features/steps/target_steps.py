from behave import given, when, then
from selenium.webdriver.common.by import By
from time import sleep

BASE_URL = "https://www.target.com/"

# ---------- Helpers ----------
def _click(driver, by, value):
    el = driver.find_element(by, value)
    el.click()
    return el

def _type(driver, by, value, text):
    el = driver.find_element(by, value)
    el.clear()
    el.send_keys(text)
    return el

# ---------- Common ----------
@given("I open the Target homepage")
def open_home(context):
    context.driver.get(BASE_URL)
    # allow page shell to render basic elements
    sleep(2)

@when('I search for "{term}"')
def search_for(context, term):
    # Search input has id="search"
    _type(context.driver, By.ID, "search", term)
    # Search button uses data-test on many builds
    _click(context.driver, By.CSS_SELECTOR, 'button[data-test="@web/Search/SearchButton"]')
    sleep(3)  # let results load a bit

@then('I see results for "{term}"')
def verify_results(context, term):
    # One robust way: verify the query chip or results header contains the term
    # Try common patterns; fall back to page text search if needed.
    possible_locators = [
        (By.CSS_SELECTOR, '[data-test="resultsHeading"]'),
        (By.CSS_SELECTOR, '[data-test="lp-resultsCount"]'),
        (By.CSS_SELECTOR, '[data-test*="Query"]'),  # e.g., query chip
        (By.CSS_SELECTOR, '[data-test*="Results"]'),
    ]

    text_blob = ""
    for by, val in possible_locators:
        els = context.driver.find_elements(by, val)
        for el in els:
            txt = el.text.strip()
            if txt:
                text_blob += " " + txt.lower()

    if not text_blob:
        # fallback: collect a few product titles
        titles = context.driver.find_elements(By.CSS_SELECTOR, '[data-test="product-title"], [data-test*="ProductCard"] h3, a[data-test*="product"]')
        text_blob = " ".join([t.text.lower() for t in titles[:10]])

    assert term.lower() in text_blob, f'Expected results to mention "{term}", got: {text_blob[:200]}'

# ---------- Target Circle ----------
@given("I open the Target Circle page")
def open_circle(context):
    context.driver.get("https://www.target.com/circle")
    sleep(2)

@then("I see at least 10 benefit cells")
def verify_circle_benefits(context):
    # We intentionally use a broad selector to be resilient to class renames.
    # Count anything that looks like a benefit/tile/card on this page.
    candidates = context.driver.find_elements(
        By.CSS_SELECTOR,
        # common patterns: "benefit", "tile", "card", or data-test attributes
        '[data-test*="benefit"], [class*="benefit"], [data-test*="Tile"], [class*="tile"], [data-test*="card"], [class*="card"]'
    )
    # Also check for grid list items
    if len(candidates) < 10:
        candidates += context.driver.find_elements(By.CSS_SELECTOR, "section li, section div[role='listitem']")
    count = len(candidates)
    assert count >= 10, f"Expected at least 10 benefit cells, found {count}"

# ---------- Add to Cart ----------
@when("I open the first search result")
def open_first_result(context):
    # Click first product tile link from grid/list
    # Try common product anchors; fall back if needed
    selectors = [
        'a[data-test="product-title"], a[data-test*="ProductCard"], a[href*="/p/"]',
        '[data-test="productGrid"] a[href*="/p/"]',
        'a[href*="/p/"]',
    ]
    first_link = None
    for sel in selectors:
        links = context.driver.find_elements(By.CSS_SELECTOR, sel)
        if links:
            first_link = links[0]
            break
    assert first_link, "Could not find any product link in search results."
    context.driver.execute_script("arguments[0].click();", first_link)
    sleep(3)

@when("I add the product to the cart")
def add_product_to_cart(context):
    # Try the Add-to-cart button on PDP; Target often uses data-test="orderPickupButton" or generic add-to-cart button
    add_btn = None
    btn_selectors = [
        'button[data-test="orderPickupButton"]',
        'button[data-test*="addToCart"], button[type="button"][id*="addToCart"]',
        'button[aria-label*="Add to cart"], button:has(span:contains("Add to cart"))',  # :has may not be supported; kept as last resort hint
        'button:contains("Add to cart")',  # Selenium CSS does not support :contains, kept as conceptual fallback
    ]
    for sel in btn_selectors:
        candidates = context.driver.find_elements(By.CSS_SELECTOR, sel)
        if candidates:
            add_btn = candidates[0]
            break

    if not add_btn:
        # try a generic button on PDP action area
        action_buttons = context.driver.find_elements(By.CSS_SELECTOR, '[data-test*="fulfillment"] button, [data-test*="purchase"] button')
        add_btn = action_buttons[0] if action_buttons else None

    assert add_btn, "Add to cart button not found on product page."
    context.driver.execute_script("arguments[0].click();", add_btn)
    sleep(3)

@then("my cart has at least 1 item")
def verify_cart_items(context):
    # Open cart
    _click(context.driver, By.CSS_SELECTOR, '[data-test="@web/CartLink"]')
    sleep(3)

    # Option A: count individual cart line items
    line_items = context.driver.find_elements(By.CSS_SELECTOR, '[data-test*="cartItem"], [data-test*="LineItem"], [class*="cart"] [class*="item"]')
    if len(line_items) >= 1:
        return

    # Option B: verify total price element exists and is non-empty
    totals = context.driver.find_elements(By.CSS_SELECTOR, '[data-test*="CartTotals"] [data-test*="summary"], [data-test*="price"], [class*="total"]')
    has_price_text = any(el.text.strip() for el in totals)
    assert has_price_text, "Cart does not appear to contain items or a total."
