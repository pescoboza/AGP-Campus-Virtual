
from .. import pdfkit_config
import pdfkit
from flask import flash, redirect, render_template, url_for, make_response
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


# Generate the users pdf certofocate.
@main.route("/certificate")
@login_required
def certificate():

    rendered = render_template("certificate/certificate.html")
    pdf = pdfkit.from_string(
        rendered, False, css="app/templates/certificate/certificate.css", configuration=pdfkit_config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=Certificado Virtual - {} {} {}.pdf".format(
        current_user.first_name, current_user.paternal_last_name, current_user.maternal_last_name)

    return response
