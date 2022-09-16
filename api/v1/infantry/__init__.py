from flask import Blueprint

infantry = Blueprint("infantry", __name__)

from . import views
