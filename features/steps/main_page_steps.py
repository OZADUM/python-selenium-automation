from behave import given


@given('Open target main page')
def open_main(context):
    # context.driver.get('https://www.target.com/')
    context.app.main_page.open_main()