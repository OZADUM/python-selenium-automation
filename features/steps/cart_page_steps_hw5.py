from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

EMPTY_MSG = (By.CSS_SELECTOR, "[data-test='boxEmptyMessage'], [data-test='emptyCart']")

@then("Verify 'Your cart is empty' message is shown (HW5)")
def verify_empty_cart_msg_hw5(context):
    el = context.driver.wait.until(EC.visibility_of_element_located(EMPTY_MSG))
    text = el.text.strip().lower()
    assert "your cart is empty" in text or "cart is empty" in text, f"Unexpected message: {text}"