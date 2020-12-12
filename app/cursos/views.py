from flask import redirect, render_template, url_for, request, flash
from flask_login import login_required, current_user

from . import cursos
from ..main import main
from ..models import User, QUIZ_CODES
from .forms import MultipleChoiceQuizForm


# Relates cancer endpoint to topic code
CANCER_NAME_TOPICS = {
    "cancer-mama":           {"code": "mama", "num_questions": 3},
    "cancer-cervicouterino": {"code": "crvu", "num_questions": 3},
    "cancer-prostata":       {"code": "psta", "num_questions": 3},
    "cancer-pulmon":         {"code": "plmn", "num_questions": 3},
    "cancer-testiculo":      {"code": "tstc", "num_questions": 3},
    "diagnostico":           {"code": "diag", "num_questions": 3}
}

@cursos.route("/", methods=["GET"])
@cursos.route("/diagnostico", methods=["GET"])
#@login_required
def diagnostico():
    return cursos_base("diagnostico")

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
    template_name = "cursos/" + cancer_name.replace('-','_') + ".html"
    return render_template(template_name, topic=quiz_topic, num_questions=num_questions)