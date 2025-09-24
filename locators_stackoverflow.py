from selenium.webdriver.common.by import By

# Email input field
EMAIL_FIELD = (By.ID, "email")

# Display name field
DISPLAY_NAME_FIELD = (By.ID, "display-name")

# Password field
PASSWORD_FIELD = (By.ID, "password")

# Confirm password field
CONFIRM_PASSWORD_FIELD = (By.ID, "confirm-password")

# Sign Up button
SIGN_UP_BUTTON = (By.ID, "submit-button")

# Google sign-up button
GOOGLE_BUTTON = (By.CSS_SELECTOR, "button.s-btn__google")

# GitHub sign-up button
GITHUB_BUTTON = (By.CSS_SELECTOR, "button.s-btn__github")

# Legal agreement checkbox
TERMS_CHECKBOX = (By.NAME, "legalLinks")