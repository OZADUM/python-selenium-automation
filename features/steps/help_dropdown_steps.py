from behave import given, when, then

@given("Open Help page (default Returns & Exchanges)")
def open_help(context):
    # Opens the default Returns & Exchanges Help page and waits for dropdown
    context.app.help_page.open_help()

@when('I choose "{topic}" in the Help topics dropdown')
def choose_topic(context, topic):
    # Fuzzy match: works with visible text or value substrings, case-insensitive
    context.app.help_page.select_topic_fuzzy(topic)

@then('The Help URL contains "{url_fragment}"')
def verify_help_url(context, url_fragment):
    context.app.help_page.verify_url_contains(url_fragment)

# Optional: use in feature if the page doesn't navigate on selection
@then('Verify header is "{text}"')
def verify_header(context, text):
    context.app.help_page.verify_header(text)