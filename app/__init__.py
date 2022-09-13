import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig, config

db = SQLAlchemy()
migrate = Migrate()

secret_token = None


def create_app(environment="development"):
    app = Flask(__name__)

    global secret_token

    app.config.from_object(config[environment])

    config[environment].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    secret_token = app.config["SECRET_KEY"]

    from api.auth import auth as auth_blueprint
    from api.v1.air_force import air_force as air_force_blueprint
    from api.v1.underwater import underwater as underwater_blueprint
    from app.models.user import User

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(air_force_blueprint, url_prefix="/api/v1/air_force")
    app.register_blueprint(underwater_blueprint, url_prefix="/api/v1/underwater")

    return app
