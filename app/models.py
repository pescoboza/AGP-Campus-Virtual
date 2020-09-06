from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import mongoengine as me

from app import login

db_str_len = 64
db_hash_len = 128

######################################################################
# User models
######################################################################
# Possible values for User.occupation
user_occupations = [
    ("",""),
    ("maestro","Maestro"),
    ("estudiante", "Estudiante"),
    ("profesionista", "Profesionista"),
    ("miembro_ong", "Miembro de ONG"),
    ("otro", "Otro")
]

# Possible values for User.gender
user_genders = [
    ("", ""),
    ("H","Hombre"),
    ("M","Mujer"),
    ("O","Otro")
]

class User(UserMixin, me.Document):
    meta = {"collection":"user"}

    email = me.StringField(max_length=db_str_len, required=True)
    first_name = me.StringField(max_length=db_str_len, required=True) # Or names
    paternal_last_name = me.StringField(max_length=db_str_len, required=True)
    maternal_last_name = me.StringField(max_length=db_str_len, required=True)
    birth_date = me.DateField(required=True)
    gender = me.StringField(required=True)
    occupation = me.StringField(required=True)
    password_hash = me.StringField(max_length=db_hash_len, required=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Gets user document instance from me. Returns None if it does not exist.
    @staticmethod
    def get_user(email):
        return User.objects(email=email).first()
    
    # Creates user without saving it the database.
    @staticmethod
    def create_new_user(email, first_name, paternal_last_name, maternal_last_name, birth_date, gender, occupation, password):
        return User(email=email, 
            first_name=first_name, 
            paternal_last_name=paternal_last_name, 
            maternal_last_name=maternal_last_name,
            birth_date=birth_date,
            gender=gender,
            occupation=occupation,
            password_hash=generate_password_hash(password))

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

#####################################################################################
# Courses items
#####################################################################################

task_types = [
    "multiple_choice_quiz"
]

# Base component of a module.
class Task(me.EmbeddedDocument):
    meta = { "allow_inheritance": True }
    
    id = me.IntField(primary_key=True, unique=True, required=True)
    name = me.StringField(required=True)
    type = me.StringField(required=True)

# Modules are the top level course units that need to be completed to get certified.
class Module(me.Document):
    meta = {"collection": "module"}
    
    id = me.IntField(primary_key=True, unique=True, required=True)
    name = me.StringField(required=True)
    tasks = me.EmbeddedDocumentListField(Task)

# Component of a MultipleChoiceQuiz
class MultipleChoiceQuestion(me.EmbeddedDocument):
    text = me.StringField(required=True)
    answers = me.ListField(me.StringField(), required=True)
    correct_answer = me.IntField(required=True) # Index of answer 

class MultipleChoiceQuiz(Task): 
    questions = me.EmbeddedDocumentListField(MultipleChoiceQuestion)