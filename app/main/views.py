
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from . import main


@main.route("/")
@main.route("/index")
def index():
    return render_template("main/index.html")


@main.route("/contact")
def contact():
    return render_template("main/contact.html")


@main.route("/faq")
def faq():
    return render_template("main/faq.html")


@main.route("/certificate")
@login_required
def certificate():
    import pdfkit
    from .. import pdfkit_config

    rendered = render_template("certificate/certificate.html")
    pdf = pdfkit.from_string(
        rendered, "out.pdf", css="app/templates/certificate/certificate.css", configuration=pdfkit_config)
    return rendered
