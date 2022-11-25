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
    

@pytest.fixture
def arrange_navy_game(app_with_db):
    from app.daos.user_dao import add_user
    from app.navy.services.navy_game_service import navy_game_service 
    from app.navy.services.ship_service import ship_service
    add_user("user1", "123", "user1@user.com")
    add_user("user2", "321", "user2@user.com")
    user1 = {"user1_id":1}
    user2 = {"user2_id":2}
    navy_game_service.add(user1)
    navy_game_service.join(user2,1)