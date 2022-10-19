import json

from flask import Blueprint, Response, jsonify, request
from flask_cors import CORS
from sqlalchemy import insert, select
from werkzeug.security import generate_password_hash

from api import token_auth
from app import db
from app.models.user import User, UserSchema

users_bp = Blueprint("users", __name__, url_prefix="/users")
user_schema = UserSchema()

CORS(users_bp)


@users_bp.route("", methods=["GET"])
# @token_auth.login_required
def get_all_users():
    users = db.session.scalars(select(User)).all()
    return jsonify(user_schema.dump(users, many=True))


@users_bp.route("/<user_id>", methods=["GET"])
# @token_auth.login_required
def get_user(user_id):
    # users = User.query.filter_by(id: user_id).one()
    # user = session.query(User).filter_by(id=user_id).one()
    user = User.query.filter_by(id=user_id).first()

    return jsonify(user_schema.dump(user))
