from selenium.webdriver.common.by import By
from behave import given, when, then
from time import sleep

from target_search_test import expected_text, actual_text


@given('Open target main page')
def open_main(context):
    context.driver.get('https://www.target.com/')


@when('Search for a product')
def search_product(context):
    context.driver.find_element(By.ID, 'search').send_keys('tea')
    context.driver.find_element(By.XPATH, "//button[@data-test='@web/Search/SearchButton']").click()
    sleep(7)


@when('Click on Cart icon')
def click_cart(context):
    context.driver.find_element(By.CSS_SELECTOR, '[data-test="@web/CartLink"]').click()


@when("Click Sign In")
def click_sign_in(context):
    context.driver.find_element(By.CSS_SELECTOR, '[data-test="@web/AccountLink"]').click()
    sleep(2)


@when("From right side navigation menu, click Sign In")
def click_sign_in_menu(context):
    sleep(1)
    links = context.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/signin"], a[href*="/login"]')
    if links:
        links[0].click()
    else:
        try:
            context.driver.find_element(By.LINK_TEXT, "Sign in").click()
        except Exception:
            context.driver.find_element(By.XPATH, "//a[contains(., 'Sign in')]").click()
    sleep(2)

@then('Verify search results are shown')
def verify_search_results(context):
    actual_text = context.driver.find_element(By.XPATH, "//div[@data-test='lp-resultsCount']").text
    expected_text = 'tea'
    assert expected_text in actual_text, f'Error. Expected text {expected_text}'


@then("Verify 'Your cart is empty' message is shown")
def verify_empty_cart_msg(context):
    expected_text = 'Your cart is empty'
    actual_text = context.driver.find_element(By.CSS_SELECTOR, '[data-test="boxEmptyMsg"]').text
    assert expected_text == actual_text, f'Expected {expected_text} but got {actual_text}'


@then("Verify Sign In form opened")
def verify_sign_in_form(context):
    sleep(2)
    candidates = [
        (By.ID, "username"),
        (By.NAME, "username"),
        (By.XPATH, "//h1[contains(., 'Sign in') or contains(., 'Sign into your Target account')]"),
    ]
    found = any(context.driver.find_elements(*loc) for loc in candidates)
    assert found, "Error: Sign In form not displayed"