from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductDetailsPage(BasePage):
    COLOR_OPTIONS = (By.CSS_SELECTOR, '[data-test="colorSwatch"]')
    SELECTED_COLOR = (By.CSS_SELECTOR, '[aria-checked="true"]')

    def open_product(self, url):
        self.open_url(url)

    def click_each_color_and_verify(self):
        colors = self.finds(self.COLOR_OPTIONS)
        assert colors, "No color options found on product page"

        for i, color in enumerate(colors):
            color.click()
            selected = self.finds(self.SELECTED_COLOR)
            assert selected, f"Color {i+1} did not get selected"

from behave import given, when, then

@given('I open the product page "{url}"')
def open_product(context, url):
    context.app.product_details_page.open_product(url)

@when('I click each available color')
def click_colors(context):
    context.app.product_details_page.click_each_color_and_verify()

@then('Each color is selected successfully')
def verify_colors(context):
    # Verification is already inside the method, so just pass
    pass