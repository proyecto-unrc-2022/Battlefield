import jwt
from flask import request, jsonify
from . import auth
from app import db
from app import secret_token
from sqlalchemy import select
from app.models.user import User
from app.daos.user_dao import check_password

@auth.route('/login', methods=["POST"])
def login():
    d = request.json

    user = db.session.scalars(select(User).where(User.username == d["username"])).one_or_none()
    if not user:
        return jsonify({"error": "user not found"})

    if not check_password( d["password"].encode('utf-8'), user.password):
        raise Exception("Invalid password")

    encoded_jwt = jwt.encode({"sub": user.id, "username": user.username}, secret_token, algorithm="HS256")


    return jsonify({"token": encoded_jwt})

