from flask import Blueprint

air_force = Blueprint('air_force', __name__)

from . import views
