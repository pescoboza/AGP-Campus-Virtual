from flask import Flask

from config import DevConfig

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    return app

app = create_app(DevConfig)

# Keep this import below the app instantiation
from app.routes import *