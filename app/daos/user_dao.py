from bcrypt import checkpw, gensalt, hashpw

from app import db

from ..models.user import User


def add_user(username, password, email):
    encoded_pass = hash_password(password.encode("UTF-8"))
    user = User(username=username, password=encoded_pass, email=email)
    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return db.session.get(User, user_id)


def get_user_by_username(username):
    return db.session.query(User).filter_by(username=username).one_or_none()


def hash_password(plaintext_password):
    return hashpw(plaintext_password, gensalt())


def check_password(plaintext_password, hashed_password):
    return checkpw(plaintext_password, hashed_password)
