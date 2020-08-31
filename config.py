import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

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
    REMEMBER_COOKIE_DURATION = timedelta(minutes=15)

    # FlaskMail settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL")
    MAIL_SUPPRESS_SEND  = os.environ.get("MAIL_SUPPRESS_SEND")
    MAIL_ASCII_ATACHMENTS = os.environ.get("MAIL_ASCII_ATACHMENTS")
    MAIL_USERNAME  = os.environ.get("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    

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
    MAIL_USE_TLS = os.environ.get("DEBUG_MAIL_USE_TLS")
    MAIL_USE_SSL = os.environ.get("DEBUG_MAIL_USE_SSL")
    MAIL_SUPPRESS_SEND  = os.environ.get("DEBUG_MAIL_SUPPRESS_SEND")
    MAIL_ASCII_ATACHMENTS = os.environ.get("DEBUG_MAIL_ASCII_ATACHMENTS")
    MAIL_USERNAME  = os.environ.get("DEBUG_MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.environ.get("DEBUG_MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.environ.get("DEBUG_MAIL_PASSWORD")