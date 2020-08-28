import os
basedir = os.path.abspath(os.path.dirname(__file__))

# TODO: Add content to configuration
class Config(object):
    Env = "production"
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "terces"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "terces"