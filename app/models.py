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

QUESTION_TOPICS = (
    "tstc", # Cancer testicular
    "crvu", # Cancer cervicouterino
    "plmn", # Cancer en pulmon
    "psta", # Cancer en prostata
    "mama", # Cancer de mama
    "diag"  # Examen diagnostic0
)



class MultipleChoiceQuestion(me.Document):
    meta = {"collection":"question_bank"}

    # A question from the bank can appear on different test types. That's why a list is used.
    topic = me.ListField(me.StringField(max_length=4, choices=QUESTION_TOPICS), required=True)
    text = me.StringField(required=True)
    choices = me.ListField(me.StringField(), required=True, max_length=26)
    answer = me.IntField(required=True)

    # Document save validation. Makes sure the answer value matches the question choice number.
    def clean(self):
        if self.answer < 0 or self.answer > len(self.choices):
            raise me.errors.ValidationError("Question answer did not match a choice index.")