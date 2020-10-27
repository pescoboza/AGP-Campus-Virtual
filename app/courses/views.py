from flask import redirect, render_template, url_for, request, flash
from flask_login import login_required, current_user

from . import courses
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

def quiz_view(template, redirect_to, topic_code, num_questions=10):
    flash("[DEBUG] Quiz: {}".format(QUIZ_CODES[topic_code]["full_name"]))
    form = MultipleChoiceQuizForm.generate_random_quiz(
        topic_code, num_questions)
    score = 0

    # Fetch the user.
    user = User.objects(email=current_user.email).first()

    # Check if the user has already passed the exam.
    already_passed = user.quiz_data[topic_code]["is_passed"]
    flash("[DEBUG] Already passed quiz: {}".format(already_passed))

    if request.method == "POST":
        score = form.get_score()
        print("[DEBUG] Score: {}/{}".format(score, num_questions))
        flash("[DEBUG] Calificación: {}/{}".format(score, num_questions))

        # If the questions changed, update both max and actual user score.
        if num_questions != user.quiz_data[topic_code]["score"][1]:
            user.quiz_data[topic_code]["score"][0] = score
            user.quiz_data[topic_code]["score"][1] = num_questions
        # The highest grade is saved.
        elif score > user.quiz_data[topic_code]["score"][0]:
            user.quiz_data[topic_code]["score"][0] = score

        # Changed the is_passed attribute from the user quiz data if needed.
        if score >= QUIZ_CODES[topic_code]["score_to_pass"] and \
                not already_passed:
            user.quiz_data[topic_code]["is_passed"] = True

        user.save()
        return redirect(redirect_to)
    return render_template(template, form=form, score=score, max_score=num_questions, already_passed=already_passed)


@courses.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    return quiz_view("courses/test.html", url_for("courses.quiz"), "diag", 10)


@courses.route("/", methods=["GET", "POST"])
@courses.route("/diagnostico", methods=["GET", "POST"])
@login_required
def diagnostico():
    return quiz_view("courses/diagnostico.html", url_for("courses.diagnostico"), "diag", 10)


@courses.route("/cancer-testiculo", methods=["GET", "POST"])
@login_required
def cancer_testiculo():
    return quiz_view("courses/cancer_testiculo.html", url_for("courses.cancer_testiculo"), "tstc", 3)


@courses.route("/cancer-prostata", methods=["GET", "POST"])
@login_required
def cancer_prostata():
    return quiz_view("courses/cancer_prostata.html", url_for("courses.cancer_prostata"), "psta", 3)


@courses.route("/cancer-pulmon", methods=["GET", "POST"])
@login_required
def cancer_pulmon():
    return quiz_view("courses/cancer_pulmon.html", url_for("courses.cancer_pulmon"), "plmn", 3)


@courses.route("/cancer-mama", methods=["GET", "POST"])
@login_required
def cancer_mama():
    return quiz_view("courses/cancer_mama.html", url_for("courses.cancer_mama"), "mama", 3)


@courses.route("/cancer-cervicouterino", methods=["GET", "POST"])
@login_required
def cancer_cervicouterino():
    return quiz_view("courses/cancer_cervicouterino.html", url_for("courses.cancer_cervicouterino"), "crvu", 3)