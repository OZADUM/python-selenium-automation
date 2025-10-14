from selenium.webdriver.common.by import By

from pages.base_page import Page

class SearchResultsPage(Page):
    SEARCH_RESULTS_TXT = (By.XPATH, "//div[@data-test='lp-resultsCount']")
    FAV_ICON = (By.CSS_SELECTOR, "[data-test='FavoritesButton']")
    FAV_TT_TEXT = (By.XPATH, "//*[contains(text(), 'Click to sign in and save')]")

    def hover_fav_icon(self):
        self.hover_element(*self.FAV_ICON)

    def verify_fav_tt_shown(self):
        self.wait_until_element_appear(*self.FAV_TT_TEXT)

    def verify_search_results(self, product):
        self.verify_partial_text(product, *self.SEARCH_RESULTS_TXT)

    def verify_product_url(self, product):
        # self.verify_url(f'https://www.target.com/s?searchTerm={product}')
        self.verify_partial_url(f'searchTerm={product}')