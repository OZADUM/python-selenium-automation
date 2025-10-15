from pages.base_page import Page
from pages.cart_page import CartPage
from pages.header import Header
from pages.help_page import HelpPage
from pages.main_page import MainPage
from pages.privacy_policy_page import PrivacyPolicyPage
from pages.target_app_page import TargetAppPage
from pages.search_results_page import SearchResultsPage
from pages.sign_in_page import SignInPage


class Application:
    def __init__(self, driver):
        self.driver = driver

        # Base / shared
        self.page = Page(driver)

        # Site pages
        self.main_page = MainPage(driver)
        self.header = Header(driver)
        self.cart_page = CartPage(driver)
        self.search_results_page = SearchResultsPage(driver)
        self.help_page = HelpPage(driver)
        self.sign_in_page = SignInPage(driver)
        self.privacy_policy_page = PrivacyPolicyPage(driver)
        self.target_app_page = TargetAppPage(driver)