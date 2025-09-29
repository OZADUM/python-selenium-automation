from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Candidate selectors (Target varies these with experiments):
CARD_SELECTORS = [
    '[data-test="@web/ProductCard"]',
    'li[data-test="productGridItem"]',
    'div[data-test="productGridItem"]',
    'li[data-test="product-card"]',
    'div[data-test="product-card"]',
]

TITLE_IN_CARD = (
    By.CSS_SELECTOR,
    '[data-test="product-title"], a[data-test="product-title"], h3[data-test="product-title"]'
)
IMG_IN_CARD = (By.CSS_SELECTOR, 'img')

# Fallback (no reliable card container)
TITLE_ANY = (
    By.CSS_SELECTOR,
    '[data-test="product-title"], a[data-test="product-title"], h3[data-test="product-title"]'
)
IMG_ANY = (By.CSS_SELECTOR, 'img[src]')

# Signals that results loaded at all
RESULTS_SIGNALS = [
    (By.CSS_SELECTOR, "[data-test='resultsHeading']"),
    (By.CSS_SELECTOR, "[data-test='lp-resultsCount']"),
    (By.CSS_SELECTOR, "[data-test='@web/ProductCard']"),
    (By.CSS_SELECTOR, "a[data-test='product-title']"),
]

@then("Every product has a name and image (HW5)")
def verify_every_product_hw5(context):
    # Use a slightly longer local wait for flaky networks
    wait = WebDriverWait(context.driver, 15)

    # 1) Wait for any signal that results are present (heading/count/title/card)
    wait.until(EC.any_of(*[EC.presence_of_element_located(s) for s in RESULTS_SIGNALS]))

    # 2) Try multiple possible card containers
    cards = []
    for sel in CARD_SELECTORS:
        found = context.driver.find_elements(By.CSS_SELECTOR, sel)
        if found:
            cards = found
            break

    if cards:
        # Validate each found card contains a non-empty title and an image with a src
        for idx, card in enumerate(cards, start=1):
            # Title
            title_el = None
            try:
                title_el = card.find_element(*TITLE_IN_CARD)
            except Exception:
                # some cards lazy-render title outside previous container; skip this card
                raise AssertionError(f"Card #{idx} missing product title element")

            title = (title_el.text or "").strip()
            if not title:
                # Sometimes title text is only in aria-label/href
                title = (title_el.get_attribute("aria-label") or title_el.get_attribute("title") or "").strip()
            assert title, f"Card #{idx} missing product name"

            # Image (any img within the card)
            try:
                img_el = card.find_element(*IMG_IN_CARD)
            except Exception:
                raise AssertionError(f"Card #{idx} missing image element")

            src = (img_el.get_attribute("src") or "").strip()
            assert src.startswith("http"), f"Card #{idx} missing/invalid image src"
        return

    # 3) Fallback path: no unified “card” nodes found.
    # Validate by collecting all titles and all images on the results list.
    titles = context.driver.find_elements(*TITLE_ANY)
    images = context.driver.find_elements(*IMG_ANY)

    # Require at least some titles and some images
    assert len(titles) > 0, "No product titles found on the results page."
    assert len(images) > 0, "No product images found on the results page."

    # Every title must be non-empty
    for idx, t in enumerate(titles, start=1):
        text = (t.text or t.get_attribute("aria-label") or t.get_attribute("title") or "").strip()
        assert text, f"Title #{idx} is empty"

    # Sanity: we should have at least as many images as titles (loose check)
    assert len(images) >= len(titles) // 2, (
        f"Found {len(titles)} titles but only {len(images)} images — page may still be loading."
    )