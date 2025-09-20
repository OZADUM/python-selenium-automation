from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('I open "{url}"')
def step_open_url(context, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    context.driver = webdriver.Chrome(options=options)
    context.driver.maximize_window()
    context.driver.get(url)

@when('I click on the Cart icon')
def step_click_cart(context):
    cart_icon = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cartIcon"))  # Target’s cart button
    )
    cart_icon.click()

@then('I should see the message "Your cart is empty"')
def step_verify_empty_cart(context):
    message = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Your cart is empty')]"))
    )
    assert "Your cart is empty" in message.text

@when('I click on "Sign In"')
def step_click_signin(context):
    signin_button = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))
    )
    signin_button.click()

@when('I click on "Sign In" from the right side navigation menu')
def step_click_signin_menu(context):
    signin_link = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Sign in']"))
    )
    signin_link.click()

@then('I should see the Sign In form')
def step_verify_signin_form(context):
    form = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))  # email/username field
    )
    assert form.is_displayed()

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()