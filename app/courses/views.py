from flask import redirect, render_template, url_for, request, flash
from flask_login import login_required, current_user

from . import courses
from ..models import User
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
    form = MultipleChoiceQuizForm.generate_random_quiz(topic_code, num_questions)
    score = 0
    if request.method == "POST":
        score = form.get_score()
        print("[DEBUG] Score: {}/{}".format(score, num_questions))
        flash("[DEBUG] Calificación: {}/{}".format(score, num_questions))
        
        # Update user's grade on the quiz.
        user = User.objects(email=current_user.email).first()
        
        if  num_questions != user.quiz_data[topic_code]["score"][1]:
            user.quiz_data[topic_code]["score"][0] = score
            user.quiz_data[topic_code]["score"][1] = num_questions
        elif score > user.quiz_data[topic_code]["score"][0]:
            user.quiz_data[topic_code]["score"][0] = score

        user.save()
        return redirect(redirect_to)
    return render_template(template, form=form, score=score, max_score=num_questions)

@courses.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    return quiz_view("courses/test.html", url_for("courses.quiz"), "diag", 10)

@courses.route("/", methods=["GET", "POST"])
@courses.route("/diagnostico", methods=["GET", "POST"])
@login_required
def diagnostico():
    return quiz_view("courses/diagnostico.html", url_for("courses.diagnostico"), "diag", 10)


@courses.route("/cancer-testicular", methods=["GET", "POST"])
@login_required
def cancer_testicular():
    return quiz_view("courses/cancer_testicular.html", url_for("courses.cancer_testicular"), "tstc", 3)

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