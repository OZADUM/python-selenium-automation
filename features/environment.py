# features/environment.py
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from app.application import Application

USE_BS = os.getenv("BEHAVE_USE_BROWSERSTACK") == "1"
BS_USERNAME = os.getenv("BSTACK_USERNAME") or os.getenv("BROWSERSTACK_USERNAME")
BS_ACCESS_KEY = os.getenv("BSTACK_ACCESS_KEY") or os.getenv("BROWSERSTACK_ACCESS_KEY")

def _start_local_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # optional
    return webdriver.Chrome(options=options)

def _start_browserstack_driver(scenario_name: str):
    if not (BS_USERNAME and BS_ACCESS_KEY):
        raise RuntimeError(
            "BrowserStack credentials missing. Set BSTACK_USERNAME and BSTACK_ACCESS_KEY "
            "(or BROWSERSTACK_USERNAME/BROWSERSTACK_ACCESS_KEY)."
        )

    # Capabilities-based auth (no creds in URL)
    options = Options()
    options.set_capability("browserName", "Chrome")
    options.set_capability("browserVersion", "latest")

    bstack_options = {
        "os": "Windows",
        "osVersion": "11",
        "sessionName": scenario_name,
        "buildName": "HW8",
        "local": "false",
        "debug": "true",
        "networkLogs": "true",

        # <<< AUTH GOES HERE >>>
        "userName": BS_USERNAME,
        "accessKey": BS_ACCESS_KEY,
    }
    options.set_capability("bstack:options", bstack_options)

    # Use the recommended hub-cloud hostname
    remote_url = "https://hub-cloud.browserstack.com/wd/hub"
    return webdriver.Remote(command_executor=remote_url, options=options)

def browser_init(context, scenario_name):
    try:
        context.driver = _start_browserstack_driver(scenario_name) if USE_BS else _start_local_driver()
    except (RuntimeError, WebDriverException) as e:
        print(f"[ENV] WebDriver init failed: {e}")
        context.driver = None
        raise

    try:
        context.driver.maximize_window()
    except Exception:
        pass

    context.driver.implicitly_wait(5)
    context.driver.wait = WebDriverWait(context.driver, 10)
    context.app = Application(context.driver)

def before_scenario(context, scenario):
    print("\nStarted scenario: ", scenario.name)
    browser_init(context, scenario.name)

def after_scenario(context, feature):
    drv = getattr(context, "driver", None)
    if drv:
        drv.quit()