from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import DevConfig

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    return app

app = create_app(DevConfig)

# Keep this import below the app instantiation
from app import routes, models