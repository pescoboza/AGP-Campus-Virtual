import os

from config import current_config
from app import create_app

app = create_app(current_config)

if __name__=="__main__":
    app.run()