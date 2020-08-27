import os

# TODO: Add content to configuration
class Config(object):
    Env = "production"
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "terces"
    

class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "terces"