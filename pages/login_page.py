from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    TERMS_LINK_BY_PARTIAL_TEXT = (By.PARTIAL_LINK_TEXT, 'Terms')
    TERMS_LINK_BY_SELECTOR = (By.CSS_SELECTOR, "a[href*='terms-conditions']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get('https://www.target.com/orders?lnk=acct_nav_my_account')
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    def click_terms(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.TERMS_LINK_BY_PARTIAL_TEXT)).click()
        except Exception:
            self.wait.until(EC.element_to_be_clickable(self.TERMS_LINK_BY_SELECTOR)).click()
