from selenium.webdriver.common.by import By
from behave import given, when, then

SEARCH_RESULTS_TXT = (By.XPATH, "//div[@data-test='lp-resultsCount']")


@then('Verify search results are shown for {product}')
def verify_search_results(context, product):
    actual_text = context.driver.find_element(*SEARCH_RESULTS_TXT).text
    assert product in actual_text, f'Error. Expected text {product} but got {actual_text}'