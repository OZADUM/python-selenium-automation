from selenium.webdriver.common.by import By
from behave import given, when, then
from time import sleep


CART_EMPTY_MSG = (By.CSS_SELECTOR, '[data-test="boxEmptyMsg"]')


@then("Verify 'Your cart is empty' message is shown")
def verify_empty_cart_msg(context):
    expected_text = 'Your cart is empty'
    actual_text = context.driver.find_element(*CART_EMPTY_MSG).text
    assert expected_text == actual_text, f'Expected {expected_text}, but got {actual_text}'