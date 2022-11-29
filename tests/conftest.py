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
def app_with_plane_data(app_with_db):
    from app.models.airforce.plane import Plane, Projectile
    plane = Plane(name="avion", size=3, speed=2, health=100, cant_projectile=3)
    db.session.add(plane)
    db.session.commit()
    plane = Plane.query.filter_by(name="avion").first()
    projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
    db.session.add(projectile)
    db.session.commit()
    yield app_with_db
    db.session.execute(delete(Projectile))
    db.session.commit()
    db.session.execute(delete(Plane))
    db.session.commit()

    



