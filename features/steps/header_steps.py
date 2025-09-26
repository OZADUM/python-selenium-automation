from selenium.webdriver.common.by import By
from behave import given, when, then
from time import sleep


SEARCH_FIELD = (By.ID, 'search')
SEARCH_BTN = (By.XPATH, "//button[@data-test='@web/Search/SearchButton']")
CART_ICON = (By.CSS_SELECTOR, '[data-test="@web/CartLink"]')
HEADER_LINKS = (By.CSS_SELECTOR, '[data-test*="@web/GlobalHeader/UtilityHeader/"]')


@when('Search for {search_word}')
def search_product(context, search_word):
    context.driver.find_element(*SEARCH_FIELD).send_keys(search_word)
    context.driver.find_element(*SEARCH_BTN).click()
    sleep(9)


@when('Click on Cart icon')
@when('Click on Cart icon')
def click_cart(context):
    context.driver.find_element(*CART_ICON).click()


@then('Verify header has {expected_amount} links')
def verify_header_link_count(context, expected_amount):
    expected_amount = int(expected_amount)
    links = context.driver.find_elements(*HEADER_LINKS)
    print(f'Links {links}')
    assert len(links) == expected_amount, f'Expected {expected_amount} links but got {len(links)}'

#
# @then('Verify header has links')
# def verify_header_link_count(context):
#     context.driver.find_element(*HEADER_LINKS)
