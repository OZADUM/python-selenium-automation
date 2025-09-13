from selenium.webdriver.common.by import By

from pages.base_page import Page

class SearchResultsPage(Page):
    SEARCH_RESULTS_TXT = (By.XPATH, "//div[@data-test='lp-resultsCount']")

    def verify_search_results(self, product):
        actual_text = self.find_element(*self.SEARCH_RESULTS_TXT).text
        assert product in actual_text, f'Error. Expected text {product} but got {actual_text}'
