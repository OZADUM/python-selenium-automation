from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Start the browser
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.google.com/")

# 2. Locate the search box and enter query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("car")
search_box.send_keys(Keys.RETURN)   # hit Enter to search

# 3. Wait until the URL contains the search term
WebDriverWait(driver, 10).until(
    EC.url_contains("car")
)

# 4. Assertion
assert "car" in driver.current_url.lower(), \
    f"Expected query not in {driver.current_url.lower()}"

print("Test passed. URL contains 'car'.")

driver.quit()