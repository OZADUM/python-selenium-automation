# HW8 – Window Handling + BrowserStack Integration

## 🎯 Objective
Implement and validate window handling in Selenium using the Target sign-in page, and run the scenario both locally and remotely on BrowserStack Automate.

---

## 🧪 Scenario
**Feature file:** `features/tests/window_handling.feature`

**Scenario:**  
`User can open and close Terms and Conditions from sign in page`

### Steps:
1. Open Target sign-in page  
2. Store original window handle  
3. Click on “Terms and Conditions” link  
4. Detect if a new tab or window opened  
5. Switch to the new window and verify “Terms and Conditions” page is displayed  
6. Close the new window and return to the original window  

---

## ⚙️ Key Implementations

### 🧩 File: `features/steps/window_handling_steps.py`
- Handles **both same-tab and new-tab** behaviors.
- Uses explicit waits with `EC.new_window_is_opened()` and fallback JS handling.
- Verifies URL/title to confirm correct page.
- Closes the new window and returns to original handle.

### 🌐 File: `features/environment.py`
- Supports **local Chrome driver** and **BrowserStack Automate**.
- Controlled by environment variable:
  ```bash
  export BEHAVE_USE_BROWSERSTACK=1
