from pages.base_page import Page
from pages.cart_page import CartPage
from pages.header import Header
from pages.main_page import MainPage
from pages.search_results_page import SearchResultsPage
from pages.side_nav_menu import SideNavMenu          # NEW
from pages.sign_in_page import SignInPage            # NEW


class Application:

    def __init__(self, driver):
        self.driver = driver

        self.page = Page(driver)
        self.cart_page = CartPage(driver)
        self.header = Header(driver)
        self.main_page = MainPage(driver)
        self.search_results_page = SearchResultsPage(driver)
        self.side_nav = SideNavMenu(driver)  # NEW
        self.sign_in_page = SignInPage(driver)  # NEW