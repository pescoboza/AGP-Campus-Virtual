
import datetime
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


COURSE_CERT = {
    "cancer-cerviouterino": {
        "cert_bg_img": "../../static/img/certificate_cervicouterino.png",
        "cert_course_name": "Cáncer Cervicouterino"
    },
    "cancer-mama": {
        "cert_bg_img": "../../static/img/certificate_mama.png",
        "cert_course_name": "Cáncer de Mama"
    },
    "cancer-testiculo": {
        "cert_bg_img": "../../static/img/certificate_testicular.png",
        "cert_course_name": "Cáncer de Testículo"
    },
    "cancer-prostata": {
        "cert_bg_img": "../../static/img/certificate_prostata.png",
        "cert_course_name": "Cáncer de Próstata"
    },
    "cancer-pulmon": {
        "cert_bg_img": "../../static/img/certificate_pulmon.png",
        "cert_course_name": "Cáncer de Pulmón"
    }
}


@main.route("/test-certificate/<name>")
@login_required
def test_certificate(name):

    # Validate that a valid url argument for course name was entered
    if name not in COURSE_CERT:
        return redirect(url_for("main.index"))

    # Shorthand for current_user
    cu = current_user

    # Get the certificate data: name, date, course, and background image
    cert_name = (
        cu.first_name + ' ' + cu.paternal_last_name + ' ' + cu.maternal_last_name).upper()
    cert_date = datetime.date.today()
    cert_date = "{}/{}/{}".format(today.day, today.month, today.year)
    cert_course_name = COURSE_CERT[name]["cert_course_name"]
    cert_bg_img = COURSE_CERT[name]["cert_bg_img"]

    rendered = render_template("certificate/_certificate.html",
                               name=cert_name,
                               date=cert_date,
                               course_name=cert_course_name,
                               background=cert_bg_img)

    pdf = pdfkit.from_string(
        rendered, False, css="app/templates/certificate/certificate.css", configuration=pdfkit_config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=Certificado Campus Virtual - {} {} {}.pdf". format(
        cu.first_name, cu.paternal_last_name, cu.maternal_last_name)

    return response


# TODO: Remove deprecated view.
# @main.route("/faq")
# def faq():
#     return render_template("main/faq.html")
