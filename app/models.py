from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

db_str_len = 64
db_hash_len = 128

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(db_str_len), index=True, unique=True)
    first_name = db.Column(db.String(db_str_len))
    last_name = db.Column(db.String(db_str_len))
    password_hash = db.Column(db.String(db_hash_len))



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Print function
    def __repr__(self):
        return "<User email:{}>".format(self.email)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))