from flask import Flask

app = Flask(__name__)

from auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
