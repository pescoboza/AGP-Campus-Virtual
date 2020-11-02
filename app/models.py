import json
import random
from datetime import datetime
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
USER_OCCUPATIONS = [
    ("", ""),
    ("maestro", "Maestro"),
    ("estudiante", "Estudiante"),
    ("profesionista", "Profesionista"),
    ("miembro_ong", "Miembro de ONG"),
    ("otro", "Otro")
]

# Possible values for User.gender
USER_GENDERS = [
    ("", ""),
    ("H", "Hombre"),
    ("M", "Mujer"),
    ("O", "Otro")
]

QUIZ_CODES = {
    "tstc": {"is_obligatory": True, "num_questions": 3,  "score_to_pass": 3, "full_name": "Cancer testicular"},
    "crvu": {"is_obligatory": True, "num_questions": 3,  "score_to_pass": 3, "full_name": "Cancer cervicouterino"},
    "plmn": {"is_obligatory": True, "num_questions": 3,  "score_to_pass": 3, "full_name": "Cancer en pulmon"},
    "psta": {"is_obligatory": True, "num_questions": 3,  "score_to_pass": 3, "full_name": "Cancer en prostata"},
    "mama": {"is_obligatory": True, "num_questions": 3,  "score_to_pass": 3, "full_name": "Cancer de mama"},
    "diag": {"is_obligatory": False, "num_questions": 10, "score_to_pass": 0, "full_name": "Examen diagnostico"}
}

QUESTION_TOPICS = tuple([*QUIZ_CODES])

USER_QUIZ_DATA = {
    "tstc": {  # Test code
        "score": [0, 3],  # Actual and max score.
        "is_passed": False,  # Whether the user passed the test.
    },
    "crvu": {
        "score": [0, 3],
        "is_passed": False,
    },
    "plmn": {
        "score": [0, 3],
        "is_passed": False,
    },
    "psta": {
        "score": [0, 3],
        "is_passed": False,
    },
    "mama": {
        "score": [0, 3],
        "is_passed": False,
    },
    "diag": {
        "score": [0, 10],
        "is_passed": False,
    }
}


class User(UserMixin, me.Document):
    meta = {"collection": "user"}

    # User permissions in ascending order
    USER_PERMS = {
        "certification": 0,  # Can also receive certificates
        "data": 1,  # Has access to data dashboard and report generation
        "admin": 2  # Full set of permissions
    }

    email = me.StringField(max_length=db_str_len, required=True)
    first_name = me.StringField(
        max_length=db_str_len, required=True)  # Or names
    paternal_last_name = me.StringField(max_length=db_str_len, required=True)
    maternal_last_name = me.StringField(max_length=db_str_len, required=True)
    birth_date = me.DateField(required=True)
    gender = me.StringField(required=True)
    occupation = me.StringField(required=True)
    password_hash = me.StringField(max_length=db_hash_len, required=True)
    registered_on = me.DateTimeField(required=True)

    quiz_data = me.DictField()
    is_certified = me.BooleanField(default=False)
    certified_on = me.DateTimeField()
    perm_level = me.IntField(default=User.USER_PERMS["certification"])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_perm(self, perm_tag):
        """
        Returns wether of not the user has at least the specified permission level
        identified by the given permission level tag.
        Returns None if the tag is invalid.
        """
        if perm_tag not in User.USER_PERMS:
            return None
        return self.perm_level >= User.USER_PERMS[perm_tag]

    def update_perm(self, perm_tag):
        """
        Changes the user's permissions given the matchin permission label string
        Has no effect if no matching tag is provided
        """
        if perm_tag in User.USER_PERMS:
            self.perm_level = User.USER_PERMS[perm_tag]

    def has_passed_quiz(self, quiz_code):
        """
        Tells if the user has completed succesfully the spefied quiz given a code
        Returns None if invalid quiz code
        """
        if quiz_code not in QUIZ_CODES:
            return None
        return self.quiz_data[quiz_code]["is_passed"]

    # Checks if the user has passed the needed tests to be certified.
    def can_be_certified(self):
        for qc in QUIZ_CODES:
            if QUIZ_CODES[qc]["is_obligatory"] and not self.quiz_data[qc]["is_passed"]:
                return False
        return True

    # Gives certification to the user but does not check the tests.
    def certify(self, certified_on=datetime.now()):
        self.is_certified = True
        self.certified_on = certified_on

    # Gets user document instance from me. Returns None if it does not exist.
    @staticmethod
    def get_user(email):
        return User.objects(email=email).first()

    # Creates user without saving it the database.
    @staticmethod
    def create_new_user(email, first_name, paternal_last_name, maternal_last_name, birth_date, gender, occupation, password, registered_on=datetime.now()):
        return User(email=email,
                    first_name=first_name,
                    paternal_last_name=paternal_last_name,
                    maternal_last_name=maternal_last_name,
                    birth_date=birth_date,
                    gender=gender,
                    occupation=occupation,
                    password_hash=generate_password_hash(password),
                    registered_on=registered_on,
                    quiz_data=USER_QUIZ_DATA)

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


class MultipleChoiceQuestion(me.Document):
    meta = {"collection": "question_bank"}

    # A question from the bank can appear on different test types. That's why a list is used.
    topic = me.ListField(me.StringField(
        max_length=4, choices=QUESTION_TOPICS), required=True)
    text = me.StringField(required=True)
    choices = me.ListField(me.StringField(), required=True, max_length=26)
    answer = me.IntField(required=True)

    # Document save validation. Makes sure the answer value matches the question choice number.
    def clean(self):
        if self.answer < 0 or self.answer > len(self.choices):
            raise me.errors.ValidationError(
                "Question answer did not match a choice index.")


# TODO: Upload all questions.
def qjson(filename):
    """ 
    Parses questions from given JSON file and returns the list. 
    :filename: Path to JSON file.
    :return: List of MultiepleChoiceQuestion.
    """
    questions = []
    with open(filename, 'r', encoding="utf8") as file:
        questions = json.load(file)
    for i in range(len(questions)):
        questions[i] = MultipleChoiceQuestion(**questions[i])
    return questions


# import random
# def mock_question_bank(num_questions):
#     texts = [
#         "What is your name?",
#         "Who are you?",
#         "How should I call you?",
#         "And you are...?",
#         "Who is it?",
#         "What do you like being called?",
#         "May I know your name?"]
#     choices = ["Bob", "Jeff", "Dawn", "Alexander", "Andromeda"]
#     num_choices = len(choices)

#     for _ in range(num_questions):
#         MultipleChoiceQuestion(
#             topic=[random.choice(QUESTION_TOPICS)],
#             text=random.choice(texts),
#             choices=choices,
#             answer=random.randint(0, num_choices-1)).save()
