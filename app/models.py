from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, login

db_str_len = 64
db_hash_len = 128

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

    # TODO: Test recovery tokens.
    def generate_recovery_token(self, expiration=3600):
        serializer = Serializer(current_app.config["SECRET_KEY"], expiration)
        return serializer.dumps({"confirm":self._id}).decode("utf-8")


@login.user_loader
def load_user(id):
    return User.objects(id=id).first()