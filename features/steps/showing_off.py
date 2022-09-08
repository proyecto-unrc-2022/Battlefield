from flask import url_for


@given("we have behave installed")
def step_impl(context):
    context.page = context.client.get(url_for("air_force.attack"))
    assert context.page


@when("we implement a test")
def step_impl(context):
    # raise NotImplementedError(u'STEP: When we implement a test')
    pass


@then("behave will test it for us!")
def step_impl(context):
    # raise NotImplementedError(u'STEP: Then behave will test it for us!')
    pass
