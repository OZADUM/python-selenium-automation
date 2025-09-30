from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then
from time import sleep


ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[id*='addToCartButton']")
LISTINGS = (By.CSS_SELECTOR, "[data-test='@web/site-top-of-funnel/ProductCardWrapper']")
SEARCH_RESULTS_TXT = (By.XPATH, "//div[@data-test='lp-resultsCount']")
SIDE_NAV_ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[data-test='content-wrapper'] [id*='addToCart']")
SIDE_NAV_PRODUCT_NAME = (By.CSS_SELECTOR, "[data-test='content-wrapper'] h4")
PRODUCT_IMG = (By.CSS_SELECTOR, 'img')
PRODUCT_TITLE = (By.CSS_SELECTOR, "[data-test='product-title']")


@when('Click on Add to Cart button')
 @@ -34,7 +37,24 @@ def side_nav_click_add_to_cart(context):
    context.driver.find_element(*SIDE_NAV_ADD_TO_CART_BTN).click()
    sleep(5)


@then('Verify search results are shown for {product}')
def verify_search_results(context, product):
    context.app.search_results_page.verify_search_results(product)


@then('Verify that every product has a name and an image')
def verify_products_name_img(context):
    # To see ALL listings (comment out if you only check top ones):
    # context.driver.execute_script("window.scrollBy(0,2000)", "")
    # sleep(0.5)
    # context.driver.execute_script("window.scrollBy(0,1000)", "")
    # If you ever need to scroll up, use negative numbers: context.driver.execute_script("window.scrollBy(0, -2000)", "")

    products = context.driver.find_elements(*LISTINGS)  # [WebEl1, WebEl2, WebEl3, WebEl4]

    for product in products[:8]:
        title = product.find_element(*PRODUCT_TITLE).text
        assert title, 'Product title not shown'
        print(f'🟢{title}')
        product.find_element(*PRODUCT_IMG)