from flask import Blueprint

courses = Blueprint("courses", __name__)

from .views import *