from flask import redirect, render_template, url_for, request
from flask_login import login_required

from . import courses
from .forms import MultipleChoiceQuizForm

@courses.route("/cancer-testicular")
def cancer_testicular(page_name):
    return render_template("courses/cancer_testicular.html")

@courses.route("/cancer-prostata")
def cancer_prostata(page_name):
    return render_template("courses/cancer_prostata.html")

@courses.route("/cancer-pulmon")
def cancer_pulmon(page_name):
    return render_template("courses/cancer_pulmon.html")

@courses.route("/cancer-mama")
def cancer_mama(page_name):
    return render_template("courses/cancer_mama.html")

@courses.route("/cancer-cervicouterino")
def cancer_cervicouterino(page_name):
    return render_template("courses/cancer_cervicouterino.html")