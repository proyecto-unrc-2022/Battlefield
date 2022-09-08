from flask import Flask
from ..config import config

def create_app(environment='development'):
    app = Flask(__name__)

    app.config.from_object(config[environment])
    config[environment].init_app(app)

    from ..auth import auth as auth_blueprint
    from ..api.v1.air_force import air_force as air_force_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(air_force_blueprint, url_prefix='/api/v1/air_force')

    return app

