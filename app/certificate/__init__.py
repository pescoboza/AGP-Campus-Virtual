from flask import Blueprint


certificate = Blueprint("certificate", __name__)

from . import views
