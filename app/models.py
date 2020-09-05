from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, login

db_str_len = 64
db_hash_len = 128

######################################################################
# User models
######################################################################

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

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"reset": self.email}).decode("utf-8")

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        user = User.objects(email=data.get("reset")).first()
        if user is None:
            return False
        user.password_hash = generate_password_hash(new_password)
        user.save()
        return True
    
@login.user_loader
def load_user(id):
    return User.objects(id=id).first()

# Modules are the top level course units that need to be completed to get certified.
class Module(db.Document):
    meta = {"collection": "course"}
    
    id = db.IntField(primary_key=True, unique=True, required=True)
    name = db.StringField(required=True)
    tasks = db.ListField(db.StringField()) # List of modules names





#####################################################################################
# Courses items
#####################################################################################

# Tasks are the atomic assignments that are done as part of modules.
class Task(db.Document):
    meta = {"collectoin": "task"}

    id = db.IntField(primary_key=True, unique=True, required=True)
    name = db.StringField(required=True)
    
    def get_content():
        raise NotImplementedError("TODO: Implement virtual function to load content from all tasks.")

class MultipleChoiceQuiz(Task):
    questions = db.ListField(db.EmbeddedDocumentField(MultipleChoiceQuestion))


class MultipleChoiceQuestion(db.Document):
    text = dg.StringField(required=True)
    answers = db.ListField(db.StringField(), required=True)
    correct_answer = db.IntField(required=True)