# features/steps/cart_page_steps.py
from behave import when, then

# --- Navigation ---

@when('Open cart page')
def open_cart(context):
    context.app.cart_page.open()

# --- Assertions ---

@then('Verify cart has correct product')
def verify_product_name(context):
    assert hasattr(context, "product_name") and context.product_name.strip(), \
        "No product_name stored in context (did you run the step that stores it?)."
    expected = context.product_name.strip()
    context.app.cart_page.verify_contains_product(expected)

@then('Verify cart has {expected:d} item(s)')
def verify_cart_items(context, expected):
    actual = context.app.cart_page.get_items_count()
    print(f"DEBUG: expected={expected}, actual={actual}, url={context.driver.current_url}")
    context.app.cart_page.verify_items_count(expected)

@then("Verify 'Your cart is empty' message is shown")
def verify_empty_cart_msg(context):
    context.app.cart_page.verify_cart_empty_msg()