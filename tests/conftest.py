import pytest
from sqlalchemy import delete

from app import create_app, db
from app.models.user import User


@pytest.fixture(scope="session")  # function, class, module, package, session
def flask_app():
    app = create_app("testing")

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope="session")
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture
def app_with_data(app_with_db):
    user = User()
    user.username = "admin"
    user.email = "admin@mail.com"
    db.session.add(user)

    db.session.commit()

    yield app_with_db

    db.session.execute(delete(User))
    db.session.commit()



