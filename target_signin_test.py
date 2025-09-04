from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# open Chrome in Incognito
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Open Target homepage
    driver.get("https://www.target.com/")
    time.sleep(2)

    # Step 2: Go straight to the Sign-In page (avoids hidden flyout clicks)
    driver.get("https://www.target.com/account")
    time.sleep(3)

    # Step 3/4: Verify heading and presence of Sign in button
    heading = driver.find_element(By.XPATH, "//h1[contains(., 'Sign in or create account')]")
    print("Heading:", heading.text)

    # Just check presence of a Sign in button
    driver.find_element(By.XPATH, "//button[contains(., 'Sign in') or @id='login']")

    print("Test Passed: Sign in page opened and required elements are present.")

except Exception as e:
    print("Test Failed:", e)

finally:
    driver.quit()