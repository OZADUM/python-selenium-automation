from selenium.webdriver.common.by import By
from behave import given, when, then
from time import sleep


CART_ICON = (By.CSS_SELECTOR, '[data-test="@web/CartLink"]')
HEADER_LINKS = (By.CSS_SELECTOR, '[data-test*="@web/GlobalHeader/UtilityHeader/"]')
TARGET_CIRCLE_HEADER = (By.CSS_SELECTOR, "[data-test='@web/Circle/PageTitle']")


@when('Search for {search_word}')
def search_product(context, search_word):
    print(search_word)
    context.app.header.search_product(search_word)


@when('Click on Cart icon')
def click_cart(context):
    context.app.header.click_cart()


@when('Click on 1st header link')
def click_1st_link(context):
    element = context.driver.find_element(*HEADER_LINKS)
    # print('Before refresh')
    # print(element)
    context.driver.refresh()
    # print('After refresh')
    element = context.driver.find_element(*HEADER_LINKS)
    # print(element)
    element.click()


@then('Verify header has {expected_amount} links')
def verify_header_link_count(context, expected_amount):
    expected_amount = int(expected_amount)
    links = context.driver.find_elements(*HEADER_LINKS)
    print(f'Links {links}')
    assert len(links) == expected_amount, f'Expected {expected_amount} links but got {len(links)}'


@then('Verify Target Circle opens')
def verify_header_link_count(context):
    context.driver.find_element(*TARGET_CIRCLE_HEADER)