import os
basedir = os.path.abspath(os.path.dirname(__file__))
MONGO_TEST_DB = "AGPCampusVirtualDev"
MONGO_TEST_URI = "mongodb+srv://admin:fractalchargeimplosion@devcluster.k7j3g.mongodb.net/AGPCampusVirtualDev?retryWrites=true&w=majority"

class Config(object):
    ENV = "production"
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    MONGODB_SETTINGS = {
        "db": os.environ.get("MONGO_DB") or MONGO_TEST_DB,
        "host": os.environ.get("MONGO_URI") or MONGO_TEST_URI,
    }        


    # Deprecated SQLalchemy code
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
    #     "sqlite:///" + os.path.join(basedir, "app.db")
    # SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "terces"

    MONGODB_SETTINGS = {
        "db": MONGO_TEST_DB,
        "host": MONGO_TEST_URI,
    }        