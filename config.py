import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    ENV = "production"
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    MONGO_DBNAME = os.environ.get("MONGO_DBNAME")
    MONGO_URI = os.environ.get("MONGO_URI")


    # Deprecated SQLalchemy code
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
    #     "sqlite:///" + os.path.join(basedir, "app.db")
    # SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "terces"

    MONGO_DBNAME = "dbdev"
    MONGO_URI = \
        "mongodb+srv://admin:fractalchargeimplosion@devcluster.k7j3g.mongodb.net/devdb?retryWrites=true&w=majority"