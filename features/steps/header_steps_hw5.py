from behave import given, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

TARGET_HOME = "https://www.target.com/"
ACC_LINK = (By.CSS_SELECTOR, '[data-test="@web/AccountLink"]')
CART_LINK = (By.CSS_SELECTOR, '[data-test="@web/CartLink"]')
RIGHT_DRAWER = (By.CSS_SELECTOR, '[data-test="accountNav"]')
SIGN_IN_LINK = (By.LINK_TEXT, "Sign in")

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

@given('Open Target home (HW5)')
def open_main_hw5(context):
    context.driver.get(TARGET_HOME)
    context.driver.wait.until(EC.visibility_of_element_located(ACC_LINK))

@when('Click Cart icon (HW5)')
def click_cart_hw5(context):
    safe_click(context, CART_LINK)

@when('Click Sign In (HW5)')
def click_sign_in_icon_hw5(context):
    safe_click(context, ACC_LINK)
    context.driver.wait.until(EC.visibility_of_element_located(RIGHT_DRAWER))

@when('From right menu, click Sign In (HW5)')
def click_sign_in_menu_hw5(context):
    context.driver.wait.until(EC.visibility_of_element_located(RIGHT_DRAWER))
    safe_click(context, SIGN_IN_LINK)