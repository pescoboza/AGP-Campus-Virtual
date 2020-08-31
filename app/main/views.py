from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from . import main

@main.route("/")
@main.route("/index")
def index():
    return render_template("index.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/faq")
def faq():
    return render_template("faq.html")