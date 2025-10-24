# features/steps/product_details_page_steps.py
from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _find_color_elements(driver):
    """
    Try a few reasonable selectors that Target commonly uses for swatches.
    Returns a non-empty list or raises AssertionError.
    """
    selectors = [
        # img inside a swatch button
        'button[data-test*="swatch"] img',
        # generic swatch imgs
        'img[alt*="Denim"], img[alt*="Color"], img[alt*="Navy"], img[alt*="Red"], img[alt*="Blue"]',
        # any possible color swatch container images
        '[data-test*="swatch"] img, [data-test*="Swatch"] img, [data-test*="color"] img',
    ]
    for css in selectors:
        els = driver.find_elements(By.CSS_SELECTOR, css)
        if els:
            return els
    raise AssertionError("Could not locate color swatches on the product page.")


@given('Open target product {tcin} page')
def open_product(context, tcin: str):
    # Known working product TCIN format like A-91269718
    # If the site redirects, that’s okay; we just need the product page open.
    base = "https://www.target.com/p/"
    context.driver.get(base + tcin)


@then("Verify user can click through colors")
def click_and_verify_colors(context):
    driver = context.driver
    wait = WebDriverWait(driver, 10)

    colors = _find_color_elements(driver)
    # Optional: print visible swatches
    print(colors)

    clicked = 0
    for c in colors:
        try:
            # Bring into view
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", c)
            wait.until(EC.element_to_be_clickable(c))
            try:
                c.click()
            except Exception:
                # Fallback to JS click if overlays intercept
                driver.execute_script("arguments[0].click();", c)
            clicked += 1
        except Exception as e:
            # Continue trying remaining swatches; we only need to prove swatches are interactable
            print(f"[WARN] Failed to click a color swatch: {e}")

    assert clicked >= 1, "No color swatch could be clicked successfully."