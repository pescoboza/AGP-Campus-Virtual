from app import db

db_str_len = 64
db_hash_len = 128

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(db_str_len), index=True, unique=True)
    first_name = db.Column(db.String(db_str_len))
    last_name = db.Column(db.String(db_str_len))
    password_hash = db.Column(db.String(db_hash_len))

    # Print function
    def __repr__(self):
        return "<User email:{}>".format(self.email)