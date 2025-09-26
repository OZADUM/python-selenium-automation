from behave import given, when, then


@given('Open Help page for Returns')
def click_cart(context):
    context.app.help_page.open_help_returns()


@when('Select Help topic {help_topic}')
def select_promotions(context, help_topic):
    context.app.help_page.select_promotions(help_topic)


@then('Verify help {expected_header_text} page opened')
def verify_help_page_opened(context, expected_header_text):
    context.app.help_page.verify_header(expected_header_text)


# @then('Verify help Returns page opened')
# def verify_returns_opened(context):
#     context.app.help_page.verify_returns_opened()
#
#
# @then('Verify help Current promotions page opened')
# def verify_promotions_opened(context):
#     context.app.help_page.verify_promotions_opened()