import os
import io
import time
import json
from threading import Thread
import datetime
from werkzeug.utils import secure_filename
from flask import current_app, flash, request, redirect, render_template, url_for, make_response, send_file, after_this_request
from flask_login import current_user, login_user, logout_user, login_required

from . import main
from ..models import User, upload_questions_from_JSON
from ..user_report import generate_user_report


@main.route("/")
@main.route("/index")
def index():
    return redirect(url_for("cursos.diagnostico"))


@main.route("/contacto")
def contact():
    return render_template("main/contact.html")


@main.route("/tablero-datos")
@login_required
def data_dashboard():
    """Displays data dashboard. Needs data or admin user role."""

    # Fetch and validate user for admin rights
    user = User.objects(email=current_user.email).first()
    if user is None or not user.has_perm("data"):
        flash("Debe contar con los permisos necesarios para acceder a esta página.")
        return redirect(url_for("main.index"))

    return render_template("main/data_dashboard.html")



@main.route("/descargar-reporte")
@login_required
def download_report():
    """Generates csv reports from user data and downloads it for the user."""

    # Fetch and validate user
    user = User.objects(email=current_user.email).first()
    if user is None or not user.has_perm("data"):
        flash("Debe contar con los permisos necesarios para acceder a esta página.")
        return redirect(url_for("main.index"))

    file_data = None
    temp_file_filename = None
    try:
        temp_file_filename = generate_user_report("user_report")

        # Read temporary file in to bitstream and delete it
        file_data = io.BytesIO()
        with open(temp_file_filename, "rb") as ifstream:
            file_data.write(ifstream.read())
        file_data.seek(0)

    except Exception as e:
        print("[ERROR] {}".format(e))

    else:
        print("[INFO] Generated user report for user with email {}".format(
            current_user.email))

    finally:
        # Remove temporary file after it is consumed
        os.remove(temp_file_filename)

    # flash("El reporte ha sido enviado.")
    return send_file(file_data, mimetype="application/csv", as_attachment=True, attachment_filename="user_report.csv")




def has_json_ext(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() == "json"

@main.route("/update-questions", methods=["GET", "POST"])
@login_required
def update_questions():
    """Send POST request with JSON file of quiz questions to update the quetion bank."""

    # Fetch and validate user for admin rights
    user = User.objects(email=current_user.email).first()
    if user is None or not user.has_perm("data"):
        flash("Debe contar con los permisos necesarios para acceder a esta página.")
        return redirect(url_for("main.index"))

    
    # Get the uploaded file from the request header and validate
    if request.method == "POST":

        # If no filename, redirect to current and flash the error
        if "file" not in request.files:
            flash("Ningún archivo seleccionado.")
            return redirect(request.url)
        
        # Validat the file and filename
        uploaded_file = request.files["file"]
        if uploaded_file and has_json_ext(uploaded_file.filename):
            
            # Save filename with dymamiccally generated name
            save_filename = "{}_upload{}_{}".format(
                user.email,
                str(time.time()).replace('.', ''),
                uploaded_file.filename)
            
            # Secure the filename
            save_filename = secure_filename(save_filename)
            
            # Add full path to file for uploads directory
            save_filename = os.path.join(current_app.config["UPLOAD_FOLDER"], save_filename)

            # Save the file
            uploaded_file.save(save_filename)
            try:
                # TODO: Figure out how to multithread this
                # worker = Thread(target=upload_questions_from_JSON, args=(save_filename))
                # worker.start()
                upload_questions_from_JSON(save_filename)
            
            except json.decoder.JSONDecodeError as e:
                flash("Error de sintaxis: {}".format(e))

            else:
                flash("El banco de preguntas ha sido actualizado.")    

            finally: 
                try:
                    os.remove(save_filename)
                except Exception:
                    pass

            return redirect(request.url)
    
    code_body = render_template("formato_preguntas.jsonc")
    return render_template("main/update_questions.html", code_body=code_body)


@main.route("/politica-de-privacidad", methods=["GET"])
def privacy_policy():
    return render_template("main/privacy_policy.html")

@main.route("/terminos-y-condiciones", methods=["GET"])
def terms_and_conditions():
    return render_template("main/terms_and_conditions.html")
