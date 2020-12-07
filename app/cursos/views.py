from flask import redirect, render_template, url_for, request, flash
from flask_login import login_required, current_user

from . import cursos
from ..main import main
from ..models import User, QUIZ_CODES
from .forms import MultipleChoiceQuizForm

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


# def quiz_view(template, redirect_to, topic_code, num_questions=10, certificate_endpoint=None):
#     # flash("[DEBUG] Quiz: {}".format(QUIZ_CODES[topic_code]["full_name"]))
#     form = MultipleChoiceQuizForm.generate_random_quiz(
#         topic_code, num_questions)
#     score = 0

#     # Fetch the user.
#     user = User.objects(email=current_user.email).first()

#     # Check if the user has already passed the exam.
#     already_passed = user.quiz_data[topic_code]["is_passed"]
#     # flash("[DEBUG] Already passed quiz: {}".format(already_passed))

#     if request.method == "POST":
#         score = form.get_score()
#         print("[DEBUG] Score: {}/{}".format(score, num_questions))
#         # flash("[DEBUG] Calificación: {}/{}".format(score, num_questions))

#         # If the questions changed, update both max and actual user score.
#         if num_questions != user.quiz_data[topic_code]["score"][1]:
#             user.quiz_data[topic_code]["score"][0] = score
#             user.quiz_data[topic_code]["score"][1] = num_questions
#         # The highest grade is saved.
#         elif score > user.quiz_data[topic_code]["score"][0]:
#             user.quiz_data[topic_code]["score"][0] = score

#         # Changed the is_passed attribute from the user quiz data if needed.
#         if score >= QUIZ_CODES[topic_code]["score_to_pass"] and \
#                 not already_passed:
#             user.quiz_data[topic_code]["is_passed"] = True

#         user.save()
#         flash("Felicidades, ha pasado el examen. Consulte el examen para descargar su certificado.")
#         return redirect(redirect_to)
#     return render_template(template, form=form, score=score, max_score=num_questions, already_passed=already_passed, certificate_endpoint=certificate_endpoint)


# # @cursos.route("/", methods=["GET", "POST"])
# @cursos.route("/diagnostico", methods=["GET", "POST"])
# # @login_required
# def diagnostico():
#     # Diagnostic has 10 questions, a topic code "diag" and no certificate
#     num_questions = 10
#     topic_code = "diag"
#     certificate_endpoint = None

#     # Logged in users get the same treatment as a regular graded quiz
#     if not current_user.is_anonymous:
#         return quiz_view("cursos/diagnostico.html", url_for("cursos.diagnostico"), topic_code, num_questions, certificate_endpoint=certificate_endpoint)

#     # Temporary quiz data for anonymous users
#     score = 0
#     form = MultipleChoiceQuizForm.generate_random_quiz(
#         topic_code, num_questions)

#     if request.method == "POST":
#         score = form.get_score()
#         print("[DEBUG] Score: {}/{}".format(score, num_questions))

#     return render_template("/cursos/diagnostico.html",
#                            form=form,
#                            score=score,
#                            max_score=num_questions,
#                            alredy_passed=False,
#                            certificate_endpoint=certificate_endpoint)


# @cursos.route("/cancer-testiculo", methods=["GET", "POST"])
# @login_required
# def cancer_testiculo():
#     return quiz_view("cursos/cancer_testiculo.html", url_for("cursos.cancer_testiculo"), "tstc", 3, certificate_endpoint="cancer-testiculo")


# @cursos.route("/cancer-prostata", methods=["GET", "POST"])
# @login_required
# def cancer_prostata():
#     return quiz_view("cursos/cancer_prostata.html", url_for("cursos.cancer_prostata"), "psta", 3, certificate_endpoint="cancer-prostata")


# @cursos.route("/cancer-pulmon", methods=["GET", "POST"])
# @login_required
# def cancer_pulmon():
#     return quiz_view("cursos/cancer_pulmon.html", url_for("cursos.cancer_pulmon"), "plmn", 3, certificate_endpoint="cancer-pulmon")


# @cursos.route("/cancer-mama", methods=["GET", "POST"])
# @login_required
# def cancer_mama():
#     return quiz_view("cursos/cancer_mama.html", url_for("cursos.cancer_mama"), "mama", 3, certificate_endpoint="cancer-mama")


# @cursos.route("/cancer-cervicouterino", methods=["GET", "POST"])
# @login_required
# def cancer_cervicouterino():
#     return quiz_view("cursos/cancer_cervicouterino.html", url_for("cursos.cancer_cervicouterino"), "crvu", 3, certificate_endpoint="cancer-cervicouterino")


# Relates cancer endpoint to topic code
CANCER_NAME_TOPICS = {
    "cancer-mama":           {"code": "mama", "num_questions": 3},
    "cancer-cervicouterino": {"code": "crvu", "num_questions": 3},
    "cancer-prostata":       {"code": "psta", "num_questions": 3},
    "cancer-pulmon":         {"code": "plmn", "num_questions": 3},
    "cancer-testiculo":      {"code": "plmn", "num_questions": 3},
    "diagnostico":           {"code": "diag", "num_questions": 3}
}


@cursos.route("/diagnostico", methods=["GET"])
@login_required
def diagnostico():
    return cursos_base("diagostico")

@cursos.route("/cancer-mama", methods=["GET"])
@login_required
def cancer_mama():
    return cursos_base("cancer-mama")

@cursos.route("/cancer-prostata", methods=["GET"])
@login_required
def cancer_prostata():
    return cursos_base("cancer-prostata")

@cursos.route("/cancer-testiculo", methods=["GET"])
@login_required
def cancer_testiculo():
    return cursos_base("cancer-testiculo")

@cursos.route("/cancer-cervicouterino", methods=["GET"])
@login_required
def cancer_cervicouterino():
    return cursos_base("cancer-cervicouterino")

@cursos.route("/cancer-pulmon", methods=["GET"])
@login_required
def cancer_pulmon():
    return cursos_base("cancer-pulmon")


def cursos_base(cancer_name):
    
    if cancer_name not in CANCER_NAME_TOPICS:
        return redirect(url_for("main.index"))
    
    entry = CANCER_NAME_TOPICS[cancer_name]
    quiz_topic = entry["code"]
    num_questions = entry["num_questions"]

    return render_template("cursos/cursos_base.html", topic=quiz_topic, num_questions=num_questions)