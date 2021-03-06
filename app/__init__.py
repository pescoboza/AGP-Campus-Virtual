import os
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler


class Msg:
    # TODO: Move this to a JSON and devise a better structure.
    class Flash:
        LOGOUT_USER = "Ha cerrado sesión correctamente."
        NEW_USER = "Bienvenido {first_name}."
        INVALID_CREDENTIALS = "Correo o contraseña inválidos."
        SAME_AS_OLD_PASSWORD = "Debe utilizar una contraseña distinta a la anterior."
        INVALID_OLD_PASSWORD = "Debe introducir su antigua contraseña correctamente."
        PASSWORD_CHANGE_SUCCESFUL = "Su contraseña ha sido modificada."
        LOGIN_REQUIRED = "Inicie sesión para ingresar a esta página."
        RECOVERY_REQUEST = "Revise su correo."
        ALREADY_LOGGED_IN = "Su sesión está activa. Para cambiar de usuario, primero debe cerrar sesión."
        PASSWORD_RESET_EMAIL_SENT = "Un correo con instrucciones para reestablecer su contraseña ha sido enviado a su bandeja de entrada."

    class Mail:
        RESET_PASSWORD_SUBJECT = "Recuperación de contraseña"

    class UserRegistration:
        ERROR_REQUIRED_FIELD = "Este campo es obligatorio."
        ERROR_PASSWORD_MATCH = "Las contraseñas deben coincidir."
        ERROR_EMAIL_IN_USE = "La dirección de correo ya ha sido registrada."
        ERROR_ACCEPT_TERMS = "Debe aceptar los términos y condiciones para continuar."
        ERROR_INVALID_EMAIL = "Por favor, introduzca una dirección de correo válida."

        ERROR_PASSWORD_LENGTH = "La contraseña debe medir entre 8 y 64 caracteres."
        ERROR_PASSWORD_AT_LEAST_ONE_NUMBER = "La contraseña debe conenter al menos un número."
        ERROR_PASSWORD_AT_LEAST_ONE_UPPERCASE = "La contraseña debe conenter al menos una letra mayúscula."
        ERROR_PASSWORD_AT_LEAST_ONE_LOWERCASE = "La contraseña debe conenter al menos una letra minúscula."
        ERROR_PASSWORD_AT_LEAST_ONE_SPECIAL_CHARACTER = "La contraseña debe contener al menos un caracter especial: {}."

        ACCEPT_TERMS = "He leído y acepto los términos y condiciones."


db = MongoEngine()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = Msg.Flash.LOGIN_REQUIRED
mail = Mail()
bootstrap = Bootstrap()

# NOTE: For future maintainers:
#   Commented out the google drive 
#   functionality to make it work
#   because validation and token creation
#   runs from the local host.
#   Try to find a way to indefenitely bind a
#   Google Auth permission to the application.

# Intialize google drive service
# from .google_drive import google_drive_init
# drive = google_drive_init()

# Register all shecuder tasks
# from .tasks import TASKS
# scheduler = APScheduler()
# for task in TASKS.values():
#     scheduler.add_job(**task)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    ################
    # Register all blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .cursos import cursos as cursos_blueprint
    app.register_blueprint(cursos_blueprint, url_prefix="/cursos")

    from .certificate import certificate as certificate_blueprint
    app.register_blueprint(certificate_blueprint, url_prefix="/certificado")

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")
    ################

    ## NOTE: Se note above
    # Start the app scheduler
    # scheduler.init_app(app)
    # scheduler.start()


    # Create folders in config if they do not exist
    for folder_name in [
        app.config["UPLOAD_FOLDER"], 
        app.config["TEMP_FOLDER"], 
        app.config["SECRET_FOLDER"]]:
        if not os.path.exists(folder_name):
            try:
                os.makedirs(folder_name)
            except Exception as e:
                print("[ERROR] {}".format(e))
                print("[ERROR] Could not create dir '{}'.".format(folder_name))

            else:
                print("[INFO] Created dir '{}'".format(folder_name))

    return app
