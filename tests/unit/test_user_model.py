from app.models.user import User


def test_new_user():
    user = User(username="brucewayne", email="batman@gmail.com")
    assert user.email == "batman@gmail.com"
