import os

from config import config
from app import create_app

app = create_app(config[os.environ.get("FLASK_ENV")])
# TODO: Remove this import.
from app.tests import *
if __name__=="__main__":
    app.run()