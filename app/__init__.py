from flask import Flask
from flask_pymongo import PyMongo
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import DevConfig

db = PyMongo()
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