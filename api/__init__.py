import jwt
from flask_httpauth import HTTPTokenAuth
from sqlalchemy import select

from app import db, secret_token
from app.daos.user_dao import check_password
from app.models.user import User

token_auth = HTTPTokenAuth(scheme="Bearer")

@token_auth.verify_token
def verify_token(token):
    try:
        decoded_jwt = jwt.decode(token, secret_token, algorithms=["HS256"])
    except Exception:
        print("Unable to decode JWT")
        return None

    username = decoded_jwt["username"]
    user = db.session.scalars(
        select(User).where(User.username == username)
    ).one_or_none()
    if user:
        return user
    print(f"Unknown user {username}")
    return None

