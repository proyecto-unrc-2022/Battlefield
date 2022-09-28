from behave import fixture, use_fixture

from app import create_app, db


@fixture
def battlefield_client(context, *args, **kwargs):
    app = create_app("testing")
    app.testing = True

    context.client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    db.create_all()

    yield context.client

    db.drop_all()

    ctx.pop()


def before_feature(context, feature):
    # -- HINT: Recreate a new flaskr client before each feature is executed.
    use_fixture(battlefield_client, context)


def after_scenario(context, scenario):
    db.session.remove()
    db.drop_all()
    db.create_all()
