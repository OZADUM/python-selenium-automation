# 🧪 HW9: Help Dropdown & Invalid Password Sign-In Tests  
**Author:** Ozan Duman  
**Date:** October 2025  

---

## ✅ Overview
This homework covers two automated UI test features built using **Behave (BDD)** and **Selenium**:
1. **Help Dropdown Navigation** — validates Target Help page dropdown functionality.  
2. **Invalid Password Sign-In** — confirms an error appears when logging in with incorrect credentials.

---

## 🧩 1. Help Dropdown Navigation (`help_dropdown.feature`)

**🎯 Goal:**  
Verify each topic in the Help dropdown correctly updates the page URL with the expected query parameters.

**🔍 Steps Verified:**
1. Open Help page (default topic: “Returns & Exchanges”).  
2. Choose a topic from the dropdown.  
3. Verify the URL contains the correct fragment (e.g., `childcat=Returns`).

**📂 Files Involved:**
- **Feature:** `features/tests/help_dropdown.feature`  
- **Step Definitions:** `features/steps/help_dropdown_steps.py`  
- **Page Object:** `pages/help_page.py`

**▶️ Run Command:**
```bash
python3 -m behave -f pretty features/tests/help_dropdown.feature
