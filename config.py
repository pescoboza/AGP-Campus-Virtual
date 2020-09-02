import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

# Helper to take python boolean value from environment variables.
def get_bool_env_var(varname):
    value = os.environ.get(varname)
    if value is None:
        return None
    value = value.lower()
    if value in ("true", '1', "on"):
        return True
    if value in ("false", '0', "off"):
        return False
    raise AttributeError("Could not parse environment variable {} as boolean.".format(varname))

# Production confituration
class Config(object):
    ENV = "production"
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # FlaskMongoengine settings
    MONGODB_SETTINGS = {
        "db": os.environ.get("MONGO_DB"),
        "host": os.environ.get("MONGO_URI"),
    }        

    # FlaskLogin settings
    REMEMBER_COOKIE_DURATION = timedelta(minutes=5)

    # FlaskMail settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = get_bool_env_var("MAIL_USE_TLS")
    MAIL_USE_SSL = get_bool_env_var("MAIL_USE_SSL")
    MAIL_SUPPRESS_SEND  = get_bool_env_var("MAIL_SUPPRESS_SEND")
    MAIL_ASCII_ATACHMENTS = get_bool_env_var("MAIL_ASCII_ATACHMENTS")
    MAIL_USERNAME  = os.environ.get("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
# Development configuration
class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    
    SECRET_KEY = os.environ.get("DEBUG_SECRET_KEY")

    # FlaskMongoengine settings
    MONGODB_SETTINGS = {
        "db": os.environ.get("DEBUG_MONGO_DB"),
        "host": os.environ.get("DEBUG_MONGO_URI"),
    }        

    # FlaskMail settings
    MAIL_SERVER = os.environ.get("DEBUG_MAIL_SERVER")
    MAIL_PORT = os.environ.get("DEBUG_MAIL_PORT")
    MAIL_USE_TLS = get_bool_env_var("DEBUG_MAIL_USE_TLS")
    MAIL_USE_SSL = get_bool_env_var("DEBUG_MAIL_USE_SSL")
    MAIL_SUPPRESS_SEND  = get_bool_env_var("DEBUG_MAIL_SUPPRESS_SEND")
    MAIL_ASCII_ATACHMENTS = get_bool_env_var("DEBUG_MAIL_ASCII_ATACHMENTS")
    MAIL_USERNAME  = os.environ.get("DEBUG_MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.environ.get("DEBUG_MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.environ.get("DEBUG_MAIL_PASSWORD")


config = {
    "development": DevConfig,
    "production": Config,
    "testing": DevConfig,
    "default": DevConfig
}