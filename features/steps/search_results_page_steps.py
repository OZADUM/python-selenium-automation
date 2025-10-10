from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[id*='addToCartButton'], [data-test='addToCartButton']")
LISTINGS = (By.CSS_SELECTOR, "[data-test='@web/site-top-of-funnel/ProductCardWrapper'], [data-test='@web/ProductCard']")
SEARCH_RESULTS_TXT = (By.XPATH, "//div[@data-test='lp-resultsCount']")

# Side panel/dialog bits (when it appears)
SIDE_NAV = (By.CSS_SELECTOR, "[data-test='@web/OverlayModal'], [role='dialog']")
SIDE_NAV_ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[data-test='content-wrapper'] [id*='addToCart'], [role='dialog'] [data-test='addToCartButton'], [role='dialog'] [data-test='addToCart']")
SIDE_NAV_PRODUCT_NAME = (By.CSS_SELECTOR, "[data-test='@web/OverlayModal'] [data-test='product-title'], [role='dialog'] [data-test='product-title']")

# Fallback sources for product title (from the first card)
PRODUCT_IMG = (By.CSS_SELECTOR, "img")
PRODUCT_TITLE = (By.CSS_SELECTOR, "[data-test='product-title']")
TITLE_IN_CARD = (By.CSS_SELECTOR, "[data-test='@web/ProductCard'] [data-test='product-title'], [data-test='@web/site-top-of-funnel/ProductCardWrapper'] [data-test='product-title']")

# Alternate success signals when there is no side panel
ADDED_TO_CART_TOAST = (By.CSS_SELECTOR, "[data-test='addToCartSuccessToast'], [data-test='addToCartSuccess']")
MINI_CART_BADGE = (By.CSS_SELECTOR, "[data-test='@web/CartLink'] [data-test='cartItemCount']")


def _wait_any(driver, timeout, locators, condition):
    wait = WebDriverWait(driver, timeout)
    for how, what in locators:
        try:
            return wait.until(condition((how, what)))
        except TimeoutException:
            continue
    return None


@when('Click on Add to Cart button')
def click_add_to_cart(context):
    wait = WebDriverWait(context.driver, 12)

    # Ensure at least one product card exists
    wait.until(EC.presence_of_all_elements_located(LISTINGS))

    # Click the first visible Add to Cart
    btns = context.driver.find_elements(*ADD_TO_CART_BTN)
    assert btns, "No Add to Cart buttons found on results."
    btns[0].click()

    # Consider success if ANY of these appears: side panel, toast, or mini-cart badge
    appeared = (
        _wait_any(context.driver, 8, [SIDE_NAV], EC.visibility_of_element_located)
        or _wait_any(context.driver, 8, [ADDED_TO_CART_TOAST], EC.visibility_of_element_located)
        or _wait_any(context.driver, 8, [MINI_CART_BADGE], EC.presence_of_element_located)
    )
    assert appeared is not None, "Add to Cart did not produce any success signal (panel/toast/badge)."


@when('Store product name')
def store_product_name(context):
    """
    Prefer the side panel title if present; otherwise fall back to the first card's title.
    Normalize by stripping vendor suffix after '|'.
    """
    wait = WebDriverWait(context.driver, 6)
    raw = None

    try:
        title_el = wait.until(EC.visibility_of_element_located(SIDE_NAV_PRODUCT_NAME))
        raw = title_el.text.strip()
    except TimeoutException:
        # Fallback to first product card's title
        titles = context.driver.find_elements(*TITLE_IN_CARD)
        assert titles, "No product titles found in results."
        raw = titles[0].text.strip()

    context.product_name = (raw or "").split("|", 1)[0].strip()
    print("Product name stored (normalized):", context.product_name)


@when('Confirm Add to Cart button from side navigation')
def side_nav_click_add_to_cart(context):
    """
    If a side panel requires a second confirm (size/color), click it once.
    If there is no panel, do nothing.
    """
    wait = WebDriverWait(context.driver, 7)
    try:
        panel = wait.until(EC.visibility_of_element_located(SIDE_NAV))
        try:
            btn = wait.until(EC.element_to_be_clickable(SIDE_NAV_ADD_TO_CART_BTN))
            btn.click()
            # brief confirmation: toast or mini-cart badge
            _wait_any(context.driver, 6, [ADDED_TO_CART_TOAST, MINI_CART_BADGE], EC.presence_of_element_located)
        except TimeoutException:
            # Panel present but no confirm button needed
            pass
    except TimeoutException:
        # No side panel — nothing to confirm
        pass


@then('Verify search results are shown for {product}')
def verify_search_results(context, product):
    context.app.search_results_page.verify_search_results(product)
    context.app.search_results_page.verify_product_url(product)


@then('Verify that every product has a name and an image')
def verify_products_name_img(context):
    products = context.driver.find_elements(*LISTINGS)
    for product in products[:8]:
        title = product.find_element(*PRODUCT_TITLE).text
        assert title, 'Product title not shown'
        print(f'🟢{title}')
        product.find_element(*PRODUCT_IMG)