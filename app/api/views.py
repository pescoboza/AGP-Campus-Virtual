from random import sample, shuffle
from flask import render_template, make_response, request, jsonify
from flask_login import current_user

from . import api
from ..models import MultipleChoiceQuestion, QUESTION_TOPICS, User
from ..cursos.forms import MultipleChoiceQuizForm

# Reposnds with HTML for the flashed messages
@api.route("/flashed-messages", methods=["POST"])
def flashed_messages():
    # TODO: remove this test
    return render_template("_flash.html")


"""
QUESTION_TOPICS = (
    "tstc", # Cancer testicular
    "crvu", # Cancer cervicouterino
    "plmn", # Cancer en pulmon
    "psta", # Cancer en prostata
    "mama", # Cancer de mama
    "diag"  # Examen diagnostico
)
"""



"""
{
    "quiz_topic": "tstc",
    "num_questions": 4
}

"""

DEFAULT_QUIZ_TOPIC = "diag"
DEFAULT_NUM_QUESTIONS = 3


# Responds with JSON for random quiz given the topic code and number of questions
@api.route("/generate-quiz", methods=["GET"])
def generate_quiz():
    
    # Validate the quiz topic
    quiz_topic = request.args.get("topic", DEFAULT_QUIZ_TOPIC)
    if quiz_topic not in QUESTION_TOPICS:
        quiz_topic = DEFAULT_QUIZ_TOPIC

    # Get the number of questions
    num_questions = request.args.get("num_questions", DEFAULT_NUM_QUESTIONS)
    num_questions = int(num_questions)

    # Sample the database
    db_questions = MultipleChoiceQuestion.objects(topic=quiz_topic)
    total_num_db_questions = db_questions.count()

    # Generate the sample indexes for the db entries    
    sample_indexes = []
    if num_questions >= total_num_db_questions:
        # More entires are demanded, return all of them
        sample_indexes = [i for i in  range(total_num_db_questions)]
        shuffle(sample_indexes)
    else:
        # Valid number of entries asked
        sample_indexes = sample(range(total_num_db_questions), num_questions)
    
    questions = []
    for i in sample_indexes:
        questions.append(db_questions[i].to_json())

    return  jsonify(questions)

@api.route("/get-quiz-html", methods=["POST"])
def get_quiz_html():
    # Validate the quiz topic
    quiz_topic = request.args.get("topic", DEFAULT_QUIZ_TOPIC)
    if quiz_topic not in QUESTION_TOPICS:
        quiz_topic = DEFAULT_QUIZ_TOPIC

    # Get the number of questions
    num_questions = request.args.get("num_questions", DEFAULT_NUM_QUESTIONS)
    num_questions = int(num_questions)

    # Generate the quiz
    form = MultipleChoiceQuizForm.generate_random_quiz(topic=quiz_topic, num_questions=num_questions)
    
    # Assign the actual number of questions fetched, in case 
    # it exceeded the number of questions available in the database
    num_questions = len(form.data)

    # TODO: Change num_questions to actual value
    return render_template("cursos/_quiz.html", form=form, num_questions=num_questions)


@api.route("/user-pass-quiz", methods=["GET", "POST"]) # TODO: Remove GET request
def user_pass_quiz():
    """Used to make a user pass a quiz"""
    # Validate the quiz topic
    quiz_topic = request.args.get("topic", None)
    if quiz_topic is None or quiz_topic not in QUESTION_TOPICS:
        return make_response("INVALID_TOPIC", 400) # Quiz topic not found

    # Validate the email or return error
    email = request.args.get("email", current_user.email)
    if email is None:
        return make_response("INVALID_EMAIL", 400) # Email not found
    
    # Validate user or return error
    user = User.objects(email=email).first()
    if user is None:
        return make_response("USER_NOT_FOUND", 404) # User no found

    # Pass the user'z quiz, return success
    user.set_passed_quiz(quiz_topic, is_passed=True)
    user.save()
    return make_response("1", 200)