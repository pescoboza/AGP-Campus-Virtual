from flask import Flask
from flask_mongoengine import MongoEngine
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import DevConfig

class Message:
    class Flash:
        LOGOUT_USER = "Ha cerrado sesión correctamente."
        NEW_USER = "Bienvenido {first_name}."

    class UserRegistration:
        ERROR_PASSWORD_MATCH = "Las contraseñas deben coincidir."
        ERROR_EMAIL_IN_USE = "La dirección de correo ya ha sido registrada."
        
        ACCEPT_TERMS = "He leído y acepto los términos y condiciones."

db = MongoEngine()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    return app

# NOTE: Remember to change configuration for production.
app = create_app(DevConfig)

# Keep this import below the app instantiation
from app import routes, models