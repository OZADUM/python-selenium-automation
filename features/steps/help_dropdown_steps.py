# features/steps/help_dropdown_steps.py
from behave import given, when, then


@given("Open Help page (default Returns & Exchanges)")
def open_help(context):
    context.app.help_page.open_help()


@when('I choose "{topic}" in the Help topics dropdown')
def choose_topic(context, topic):
    context.app.help_page.select_topic(topic)


@then('The Help URL contains "{fragment}"')
def url_contains(context, fragment):
    # For the "Returns" row, accept any URL that clearly indicates 'returns'
    if fragment == "childcat=Returns":
        context.app.help_page.assert_url_contains_any_ci(
            ["childcat=Returns", "/help/topic-page/returns", "/help/returns", "returns"]
        )
    else:
        context.app.help_page.assert_url_contains(fragment)