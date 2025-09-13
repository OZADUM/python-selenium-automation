# class BasePage:
#
#     def click(self):
#         print('Clicking...')
#
#     def find_element(self, locator):
#         print('Searching...')
#         return 'FoundElement'
#
#     def verify_text(self, locator):
#         print('Verifying...')
#
#
# class LoginPage(BasePage):
#     LOGIN_BTN = ''
#
#     def find_login_btn(self):
#         self.find_element(self.LOGIN_BTN)
#
# class HomePage(BasePage):
#
#     def verify_page_opened(self):
#         self.verify_text('home header')
#
#
# login_page = LoginPage()
# element = login_page.find_login_btn()
# print(element)