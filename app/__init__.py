import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig, config

db = SQLAlchemy()
migrate = Migrate()

secret_token = None


def create_app(environment="development"):
    app = Flask(__name__)
    CORS(app)

    global secret_token

    app.config.from_object(config[environment])

    config[environment].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    secret_token = app.config["SECRET_KEY"]

    from api.auth import auth as auth_blueprint
    from api.users import users_bp as users_blueprint
    from api.v1.air_force import air_force as air_force_blueprint
    from api.v1.infantry import infantry as infantry_blueprint
    from api.v1.navy import navy as navy_blueprint
    from api.v1.underwater import underwater as underwater_blueprint
    from app.models.navy.dynamic_game import Game
    from app.models.navy.dynamic_missile import DynamicMissile
    from app.models.navy.dynamic_ship import DynamicShip
    from app.models.user import User

    app.register_blueprint(navy_blueprint, url_prefix="/api/v1/navy")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(users_blueprint, url_prefix="/api/users")
    app.register_blueprint(air_force_blueprint, url_prefix="/api/v1/air_force")
    app.register_blueprint(underwater_blueprint, url_prefix="/api/v1/underwater")
    app.register_blueprint(infantry_blueprint, url_prefix="/api/v1/infantry")

    @app.get("/")
    def index():
        return "index"

    return app
