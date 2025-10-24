# features/steps/help_page_steps.py
from behave import given, when, then


@given("Open Help page for Returns")
def open_returns(context):
    context.app.help_page.open_help_returns()


@then("Verify help Returns page opened")
def verify_returns(context):
    context.app.help_page.assert_url_contains_any_ci(
        ["/help/topic-page/returns", "childcat=Returns", "/help/returns", "returns"]
    )


@when("Select Help topic Promotions & Coupons")
def select_promotions(context):
    context.app.help_page.select_topic("Promotions & Coupons")


@then("Verify help Current promotions page opened")
def verify_promotions(context):
    context.app.help_page.assert_url_contains_ci("promotions")


@when("Select Help topic Target Circle™")
def select_circle(context):
    context.app.help_page.select_topic("Target Circle™")


@then("Verify help About Target Circle page opened")
def verify_circle(context):
    # Accept common variants Target uses for loyalty pages
    context.app.help_page.assert_url_contains_any_ci(
        ["target circle", "target-circle", "circle", "loyalty"]
    )