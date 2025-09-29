from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

SEARCH_INPUT = (By.ID, "search")
SEARCH_BTN = (By.CSS_SELECTOR, "[data-test='@web/Search/SearchButton']")
RESULTS_HEADING = (By.CSS_SELECTOR, "[data-test='resultsHeading']")
RESULTS_COUNT = (By.CSS_SELECTOR, "[data-test='lp-resultsCount']")
PRODUCT_CARD = (By.CSS_SELECTOR, "[data-test='@web/ProductCard']")

def safe_click(context, locator):
    el = context.driver.wait.until(EC.element_to_be_clickable(locator))
    try:
        el.click()
    except Exception:
        context.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            el.click()
        except Exception:
            context.driver.execute_script("arguments[0].click();", el)

@when('Search for a product (HW5)')
def search_product_default_hw5(context):
    search_for_hw5(context, "tea")

@when('I search for "{query}" (HW5)')
def search_for_hw5(context, query):
    box = context.driver.wait.until(EC.visibility_of_element_located(SEARCH_INPUT))
    box.clear()
    box.send_keys(query)
    safe_click(context, SEARCH_BTN)
    try:
        context.driver.wait.until(EC.visibility_of_element_located(RESULTS_HEADING))
    except Exception:
        try:
            context.driver.wait.until(EC.visibility_of_element_located(RESULTS_COUNT))
        except Exception:
            context.driver.wait.until(EC.presence_of_all_elements_located(PRODUCT_CARD))

@then('Verify search results are shown (HW5)')
def verify_search_results_hw5(context):
    try:
        el = context.driver.wait.until(EC.visibility_of_element_located(RESULTS_HEADING))
        assert el.text.strip() != ""
        return
    except Exception:
        pass
    try:
        el = context.driver.wait.until(EC.visibility_of_element_located(RESULTS_COUNT))
        assert el.text.strip() != ""
        return
    except Exception:
        pass
    cards = context.driver.wait.until(EC.presence_of_all_elements_located(PRODUCT_CARD))
    assert len(cards) > 0, "Expected results, but none were found."