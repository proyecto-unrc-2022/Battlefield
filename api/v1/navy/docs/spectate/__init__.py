from flask import Blueprint

spec_sw = Blueprint("spec_sw", __name__)

from . import views
