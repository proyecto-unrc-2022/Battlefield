from flask import Flask

app = Flask(__name__)

from auth import auth as auth_blueprint
from api.v1 import air_force as air_force_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(air_force_blueprint, url_prefix='/api/v1/air_force')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
