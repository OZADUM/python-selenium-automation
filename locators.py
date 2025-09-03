from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://www.amazon.com/')

# find by ID
driver.find_element(By.ID, 'twotabsearchtextbox')

# find by XPath
driver.find_element(By.XPATH, '//input[@aria-label="Search Amazon"]')
driver.find_element(By.XPATH, '//input[@placeholder="Search Amazon"]')
driver.find_element(By.XPATH, '//input[@name="field-keywords"]')

# XPath, many attr
driver.find_element(By.XPATH, '//input[@tabindex="0" and @role="searchbox"]')
driver.find_element(By.XPATH, '//input[@role="searchbox" and @tabindex="0" and....]')

# XPath, text()
driver.find_element(By.XPATH, "//a[text()='Best Sellers']")
driver.find_element(By.XPATH, "//a[text()='Best Sellers' and @href='/gp/bestsellers/?ref_=nav_cs_bestsellers']")
driver.find_element(By.XPATH, "//a[text()='Best Sellers' and @class='nav-a  ']")

# Any tag, just *
driver.find_element(By.XPATH, '//*[@aria-label="Search Amazon"]')

# Xpath, parent => child node
driver.find_element(By.XPATH, "//div[@id='nav-xshop']//a[text()='Best Sellers']")
# Contains:
driver.find_element(By.XPATH, "//a[text()='Best Sellers' and contains(@href, 'nav_cs_bestsellers')]")