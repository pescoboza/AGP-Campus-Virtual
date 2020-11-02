import os
import io
import time
import datetime
from .. import pdfkit_config
import pdfkit
from flask import flash, redirect, render_template, url_for, make_response, send_file, after_this_request
from flask_login import current_user, login_user, logout_user, login_required

from . import main
from ..models import User


@main.route("/")
@main.route("/index")
def index():
    return render_template("main/index.html")


@main.route("/contact")
def contact():
    return render_template("main/contact.html")


COURSE_CERT = {
    "cancer-cerviouterino": {
        "cert_bg_img": "certificate_cervicouterino.png",
        "cert_course_name": "Cáncer Cervicouterino",
        "quiz_code": "crvu"
    },
    "cancer-mama": {
        "cert_bg_img": "certificate_mama.png",
        "cert_course_name": "Cáncer de Mama",
        "quiz_code": "mama"

    },
    "cancer-testiculo": {
        "cert_bg_img": "certificate_testicular.png",
        "cert_course_name": "Cáncer de Testículo",
        "quiz_code": "tstc"
    },
    "cancer-prostata": {
        "cert_bg_img": "certificate_prostata.png",
        "cert_course_name": "Cáncer de Próstata",
        "quiz_code": "psta"

    },
    "cancer-pulmon": {
        "cert_bg_img": "certificate_pulmon.png",
        "cert_course_name": "Cáncer de Pulmón",
        "quiz_code": "plmn"
    }
}


@main.route("/certificate/<name>")
@login_required
def certificate(name):

    # Validate that a valid url argument for course name was entered
    if name not in COURSE_CERT:
        return redirect(url_for("main.index"))

    # Shorthand for current_user
    cu = current_user

    # Fetch the current user from the database
    user = User.objects(email=cu.email).first()
    if user == None:
        return redirect(url_for("main.index"))

    # Check if user has completed the quiz
    if not user.has_passed_quiz(COURSE_CERT[name]["quiz_code"]):
        flash("Debe completar la evaluación para obtener su certificado.")
        return redirect(url_for("courses.{}".format(name.replace('-', '_'))))

    # Current working dir to set abs path for pdfkit html resources
    cwd = os.getcwd()

    # Get the certificate data: title, user name, date, course, background image and font path
    cert_title = "Certificado Campus Virtual - {} {} {}".format(
        cu.first_name, cu.paternal_last_name, cu.maternal_last_name)
    cert_name = (
        cu.first_name + ' ' + cu.paternal_last_name + ' ' + cu.maternal_last_name).upper()
    cert_date = datetime.date.today()
    cert_date = "{}/{}/{}".format(cert_date.day,
                                  cert_date.month, cert_date.year)
    cert_course_name = COURSE_CERT[name]["cert_course_name"]
    cert_bg_img = os.path.join(
        cwd, "app/static/img", COURSE_CERT[name]["cert_bg_img"]).replace('\\', '/')
    cert_font_path = os.path.join(
        cwd, "app/static/css/fonts/").replace('\\', '/')

    # The Jinja rendered string to pass to pdf generator
    rendered = render_template("certificate/_certificate.html",
                               title=cert_title,
                               name=cert_name,
                               date=cert_date,
                               course_name=cert_course_name,
                               background=cert_bg_img,
                               font_path=cert_font_path)

    # Generate pdf payload using pdfkit
    pdf = pdfkit.from_string(
        input=rendered, output_path=False, configuration=pdfkit_config,
        options={
            "enable-local-file-access": None,
            "disable-smart-shrinking": None
        }
    )

    # Set up the pdf response headers for a pdf file instead of regular html
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename={}.pdf". format(
        cert_title)

    return response


@main.route("/data")
def data():
    """
    Admin data view.
    """

    # Fetch and validate user
    user = User.objects(email=current_user.email).first()
    if user is None or not user.has_perm("data"):
        flash("Debe contar con los permisos necesarios para acceder a esta página.")
        return redirect(url_for("main.index"))

    return render_template("/main/data.html")


@main.route("/download-report")
@login_required
def download_report():
    """
    Generates csv reports from user data.
    """

    # Fetch and validate user
    user = User.objects(email=current_user.email).first()
    if user is None or not user.has_perm("data"):
        flash("Debe contar con los permisos necesarios para acceder a esta página.")
        return redirect(url_for("main.index"))

    # CSV lines formatting
    header = "gender, occupation, registered_on, birth_date\n"
    line_template = "{g}, {o}, {r}, {b}\n"
    temp_filename = "report_tmp{}.csv".format(
        str(time.time()).replace('.', ''))  # Dynamic file linked to time

    # Generate temporary CSV file
    with open(temp_filename, 'w', encoding="utf-8") as ofile:
        ofile.write(header)
        for user in User.objects:
            line = line_template.format(
                g=user.gender,
                o=user.occupation,
                r=user.registered_on,
                b=user.birth_date)
            ofile.write(line)

    # Read temporary file in to bitstream and delete it
    file_data = io.BytesIO()
    with open(temp_filename, "rb") as ifstream:
        file_data.write(ifstream.read())
    file_data.seek(0)
    os.remove(temp_filename)

    flash("El reporte ha sido enviado.")
    return send_file(file_data, mimetype="application/csv", as_attachment=True, attachment_filename="user_report.csv")
