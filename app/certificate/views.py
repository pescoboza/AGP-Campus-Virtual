from flask import url_for, redirect, flash, make_response
from flask_login import login_required, current_user

from ..models import User
from . import certificate
from .certificate import generate_certificate, timestamp_str

CERT_ROUTES = {
    "cancer-pulmon":         "plmn",
    "cancer-mama":           "mama",
    "cancer-cervicouterino": "crvu",
    "cancer-prostata":       "psta",
    "cancer-testicular":     "tstc"
}

CERT_NAMES = {
    "cancer-pulmon":            "Cáncer de pulmón",
    "cancer-mama":              "Cáncer de mama",
    "cancer-cervicouterino":    "Cáncer cervicouterino",
    "cancer-prostata":          "Cáncer de próstata",
    "cancer-testicular":        "Cáncer testicular"
}


@certificate.route("/<name>")
@login_required
def download_certificate(name):

    # Validate that a valid url argument for course name was entered
    if name not in CERT_ROUTES:
        return redirect(url_for("errors.not_found_error"))

    topic_code = CERT_ROUTES[name]

    # Shorthand for current_user
    cu = current_user

    # Fetch the current user from the database
    user = User.objects(email=cu.email).first()
    if user == None:
        flash("Debe registrar una cuenta y aprobar la evualuación para obtener su certificado.")
        return redirect(url_for("main.index"))

    # Check if user has completed the quiz
    if not user.has_passed_quiz(topic_code):
        flash("Debe completar la evaluación al final del módulo para obtener su certificado.")
        return redirect(url_for("cursos.{}".format(name.replace('-', '_'))))

    
    
    # Current working dir to set abs path for pdfkit html resources
    cwd = os.getcwd()

    full_name = "{} {} {}".format(cu.first_name, cu.paternal_last_name, cu.maternal_last_name)
    cert_title = "Certificado de {} a {}".format(CERT_NAMES[name], full_name)
    cert_filename = cert_title + ".pdf"
    
    #"{}{}{}_{}_{}".format(cu.first_name, cu.paternal_last_name, cu.maternal_last_name, CERT_ROUTES[name], timestamp_str())

    canvas = generate_certificate(cert_filename, full_name, topic_code)

    # Generate pdf payload using pdfkit
    pdf = canvas.getpdfdata()

    # Set up the pdf response headers for a pdf file instead of regular html
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename={}.pdf". format(
        cert_title)

    return response