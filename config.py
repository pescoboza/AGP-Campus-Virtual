
# TODO: Add content to configuration
class Config(object):
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    