from dotenv import load_dotenv
# Load the environtme variables
load_dotenv()

from config import current_config
from app import create_app




# instatiate the application
app = create_app(current_config)

if __name__=="__main__":
    app.run()