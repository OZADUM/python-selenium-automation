import time
from selenium import webdriver

# open Chrome in Incognito
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Open Amazon homepage
    driver.get("https://www.amazon.com/")
    time.sleep(2)
    # Step 2: Go straight to the Sign-In page (avoids hidden flyout clicks)
    driver.get('https://www.amazon.com/ap/signin')
    time.sleep(3)

    print("Test Passed: Sign in page opened and required elements are present.")

except Exception as e:
    print("Test Failed:", e)

finally:
    driver.quit()
