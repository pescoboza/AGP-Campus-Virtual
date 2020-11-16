import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


# Helper to take python boolean value from environment variables.
def get_bool_env_var(varname):
    value = os.getenv(varname)
    if value is None:
        return None
    value = value.lower()
    if value in ("true", '1', "on"):
        return True
    if value in ("false", '0', "off"):
        return False
    raise AttributeError(
        "Could not parse environment variable {} as boolean.".format(varname))


# Production configuration
class Config(object):
    ENV = "production"
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    # FlaskMongoengine settings
    MONGODB_SETTINGS = {
        "db": os.getenv("MONGO_DB"),
        "host": os.getenv("MONGO_URI"),
    }

    # FlaskLogin settings
    REMEMBER_COOKIE_DURATION = timedelta(minutes=5)

    # FlaskMail settings
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = get_bool_env_var("MAIL_USE_TLS")
    MAIL_USE_SSL = get_bool_env_var("MAIL_USE_SSL")
    MAIL_SUPPRESS_SEND = get_bool_env_var("MAIL_SUPPRESS_SEND")
    MAIL_ASCII_ATACHMENTS = get_bool_env_var("MAIL_ASCII_ATACHMENTS")
    MAIL_SENDER = os.getenv("MAIL_SENDER")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SUBJECT_PREFIX = os.getenv("MAIL_SUBJECT_PREFIX")

    # PDFkit wkhtmltopdf location
    PDFKIT_WKHTMLTOPDF_PATH = os.getenv("PDFKIT_WKHTMLTOPDF_PATH")

    # File ipload folder
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    TEMP_FOLDER = os.getenv("TEMP_FOLDER")
    SECRET_FOLDER = os.getenv("SECRET_FOLDER")


# Development configuration
class DevConfig(Config):
    ENV = "development"
    DEBUG = True

    SECRET_KEY = os.getenv("DEBUG_SECRET_KEY")

    # FlaskMongoengine settings
    MONGODB_SETTINGS = {
        "db": os.getenv("DEBUG_MONGO_DB"),
        "host": os.getenv("DEBUG_MONGO_URI"),
    }

    # FlaskMail settings
    MAIL_SERVER = os.getenv("DEBUG_MAIL_SERVER")
    MAIL_PORT = os.getenv("DEBUG_MAIL_PORT")
    MAIL_USE_TLS = get_bool_env_var("DEBUG_MAIL_USE_TLS")
    MAIL_USE_SSL = get_bool_env_var("DEBUG_MAIL_USE_SSL")
    MAIL_SUPPRESS_SEND = get_bool_env_var("DEBUG_MAIL_SUPPRESS_SEND")
    MAIL_ASCII_ATACHMENTS = get_bool_env_var("DEBUG_MAIL_ASCII_ATACHMENTS")
    MAIL_SENDER = os.getenv("DEBUG_MAIL_SENDER")
    MAIL_USERNAME = os.getenv("DEBUG_MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.getenv("DEBUG_MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.getenv("DEBUG_MAIL_PASSWORD")
    MAIL_SUBJECT_PREFIX = os.getenv("DEBUG_MAIL_SUBJECT_PREFIX")

    # PDFkit wkhtmltopdf location
    PDFKIT_WKHTMLTOPDF_PATH = os.getenv("DEBUG_PDFKIT_WKHTMLTOPDF_PATH")

    # File ipload folder
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    TEMP_FOLDER = os.getenv("TEMP_FOLDER")
    SECRET_FOLDER = os.getenv("SECRET_FOLDER")



# Configuration environments mathing each object.
config = {
    "development": DevConfig,
    "production": Config,
    "testing": DevConfig,
    "default": DevConfig
}

current_config = config.get(os.getenv("FLASK_ENV"), config["development"])
