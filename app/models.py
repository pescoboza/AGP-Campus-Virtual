from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

db_str_len = 64
db_hash_len = 128

# TODO: Figure out if one can use flask_login UserMixin with flask_mongoengine document model
class User(UserMixin, db.Document):
    meta = {"collection":"user"}

    email = db.StringField(max_length=db_str_len, required=True)
    first_name = db.StringField(max_length=db_str_len, required=True)
    last_name = db.StringField(max_length=db_str_len, required=True)
    password_hash = db.StringField(max_length=db_hash_len, required=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Gets user document instance from db. Returns None if it does not exist.
    @staticmethod
    def get_user(email):
        return User.objects(email=email).first()
    
    # Creates user without saving it the database.
    @staticmethod
    def create_new_user(email, first_name, last_name, password):
        return User(email=email, first_name=first_name, last_name=last_name, password_hash=generate_password_hash(password))

    # Print function
    def __repr__(self):
        return "<User email:{}>".format(self.email)


@login.user_loader
def load_user(id):
    return User.objects(id=id).first()