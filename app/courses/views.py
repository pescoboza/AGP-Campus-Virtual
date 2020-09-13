from flask import redirect, render_template, url_for, request
from flask_login import login_required

from . import courses
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

def quiz_view(quiz_topic, num_questions):
    pass
@courses.route("/", methods=["GET", "POST"])
@courses.route("/diagnostico", methods=["GET", "POST"])
@login_required
def diagnostico():
    num_questions = 10
    form = MultipleChoiceQuizForm.generate_random_quiz("diag", num_questions)
    score = 0
    if request.method == "POST":
        score = form.get_score()
        print("[DEBUG]: Score: {}/{}".format(score, num_questions))
        return redirect(url_for("courses.diagnostico"))
    return render_template("courses/quiz.html", form=form, score=score, max_score=num_questions)
    #return render_template("courses/diagnostico.html", form=form, score=score, max_score=num_questions)

@courses.route("/cancer-testicular", methods=["GET", "POST"])
@login_required
def cancer_testicular():
    form = MultipleChoiceQuizForm.generate_random_quiz("tstc", 3)
    return render_template("courses/cancer_testicular.html", form=form)

@courses.route("/cancer-prostata", methods=["GET", "POST"])
@login_required
def cancer_prostata():
    form = MultipleChoiceQuizForm.generate_random_quiz("psta", 3)
    return render_template("courses/cancer_prostata.html", form=form)

@courses.route("/cancer-pulmon", methods=["GET", "POST"])
@login_required
def cancer_pulmon():
    form = MultipleChoiceQuizForm.generate_random_quiz("plmn", 3)
    return render_template("courses/cancer_pulmon.html", form=form)

@courses.route("/cancer-mama", methods=["GET", "POST"])
@login_required
def cancer_mama():
    form = MultipleChoiceQuizForm.generate_random_quiz("mama", 3)
    return render_template("courses/cancer_mama.html", form=form)

@courses.route("/cancer-cervicouterino", methods=["GET", "POST"])
@login_required
def cancer_cervicouterino():
    form = MultipleChoiceQuizForm.generate_random_quiz("crvu", 3)
    return render_template("courses/cancer_cervicouterino.html", form=form)