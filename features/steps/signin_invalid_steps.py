import os
from behave import given, when, then

# Placeholders to catch accidental literals
PLACEHOLDERS = {"__FROM_ENV__", "YOUR_REAL_TARGET_EMAIL", "youremail@domain.com"}

def _resolve_email(context, email_param):
    if email_param and "@" in email_param and email_param not in PLACEHOLDERS:
        return email_param
    return (
        context.config.userdata.get("email")
        or os.environ.get("TARGET_TEST_EMAIL")
        or ""
    )

@given("I open Target Sign In page")
def open_signin(context):
    context.app.sign_in_page.open()

@when('I enter email "{email}" and continue')
def enter_email(context, email):
    email_to_use = _resolve_email(context, email)
    print(f"[DEBUG] Using email: {email_to_use!r}")
    assert email_to_use and email_to_use not in PLACEHOLDERS, (
        "❌ No real email provided. Supply one of:\n"
        '  • behave:  -D email="you@domain.com"\n'
        '  • env var: export TARGET_TEST_EMAIL="you@domain.com"\n'
        "  • or hardcode locally in the feature."
    )
    context.app.sign_in_page.enter_email_and_continue(email_to_use)

@when('I enter password "{password}" and submit with password')
def enter_password(context, password):
    context.app.sign_in_page.enter_password_and_submit(password)

@then("I see a sign-in error message")
def verify_error(context):
    ok, evidence = context.app.sign_in_page.auth_failed_or_challenged()
    # Print current URL to help grading/debug
    print(f"[DEBUG] URL after submit: {context.driver.current_url}")
    assert ok, f"Expected an error/challenge after wrong password. Evidence: {evidence}"
    print(f"[DEBUG] Auth feedback: {evidence}")