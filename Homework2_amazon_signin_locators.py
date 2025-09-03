from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://www.amazon.com/ap/signin')

# Amazon logo
driver.find_element(By.ID, "nav-logo-sprites")
driver.find_element(By.XPATH, "//a[@id='nav-logo-sprites']")

# Email field
driver.find_element(By.ID, "ap_email")
driver.find_element(By.XPATH, "//input[@id='ap_email']")

# Continue button
driver.find_element(By.ID, "continue")
driver.find_element(By.XPATH, "//input[@id='continue']")

# Conditions of Use link
driver.find_element(By.XPATH, "//a[text()='Conditions of Use']")

# Privacy Notice link
driver.find_element(By.XPATH, "//a[text()='Privacy Notice']")

# Need help link
driver.find_element(By.XPATH, "//span[contains(text(),'Need help')]")

# Forgot your password link
driver.find_element(By.ID, "auth-fpp-link-bottom")
driver.find_element(By.XPATH, "//a[@id='auth-fpp-link-bottom']")

# Other issues with Sign-In link
driver.find_element(By.ID, "ap-other-signin-issues-link")
driver.find_element(By.XPATH, "//a[@id='ap-other-signin-issues-link']")

# Create your Amazon account button
driver.find_element(By.ID, "createAccountSubmit")
driver.find_element(By.XPATH, "//a[@id='createAccountSubmit']")


