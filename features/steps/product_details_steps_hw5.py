from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

PDP_TITLE = (By.CSS_SELECTOR, "[data-test='product-title'], h1[data-test='product-title']")
COLOR_SWATCHES = (By.CSS_SELECTOR, "[data-test='@web/SwatchColor'], [data-test='variationButton']")

def js_center(context, el):
    context.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

@given('I open the product page "{pdp_url}" (HW5)')
def open_pdp_hw5(context, pdp_url):
    context.driver.get(pdp_url)
    context.driver.wait.until(EC.visibility_of_element_located(PDP_TITLE))

@when('I click each available color (HW5)')
def click_each_color_hw5(context):
    context.driver.wait.until(EC.presence_of_element_located(COLOR_SWATCHES))
    swatches = context.driver.find_elements(*COLOR_SWATCHES)
    assert swatches, "No color swatches found on PDP."
    for i in range(len(swatches)):
        swatches = context.driver.find_elements(*COLOR_SWATCHES)
        el = swatches[i]
        js_center(context, el)
        try:
            el.click()
        except Exception:
            context.driver.execute_script("arguments[0].click();", el)
        aria = el.get_attribute("aria-checked")
        cls = (el.get_attribute("class") or "").lower()
        assert aria == "true" or "selected" in cls, f"Swatch #{i+1} did not become selected"

@then('All colors were selectable (HW5)')
def all_colors_selected_hw5(context):
    pass