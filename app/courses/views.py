from flask import redirect, render_template, url_for, request
from flask_login import login_required

from . import courses
from ..models import Module
from .forms import MultipleChoiceQuizForm

@courses.route("/")
def empty():
    return redirect(url_for("courses.dashboard"))

@courses.route("/info/<page_name>")
@courses.route("/que-es/<page_name>")
def info(page_name):
    return render_template("/courses/info/{}.html".format(page_name.replace('-','_')))

@courses.route("/symptoms/<page_name>")
@courses.route("/sintomas/<page_name>")
def symptoms(page_name):
    return render_template("/courses/symptoms/{}.html".format(page_name.replace('-','_')))

@courses.route("/prevention/<page_name>")
@courses.route("/prevencion/<page_name>")
def prevention(page_name):
    return render_template("/courses/prevention/{}.html".format(page_name.replace('-','_')))

@courses.route("/risk-factors/<page_name>")
@courses.route("/factores-de-riesgo/<page_name>")
def risk_factors(page_name):
    return render_template("/courses/risk_factors/{}.html".format(page_name.replace('-','_')))

@courses.route("/autoexamination/<page_name>")
@courses.route("/autoexaminacion/<page_name>")
def autoexamination(page_name):
    return render_template("/courses/autoexamination/{}.html".format(page_name.replace('-','_')))

@courses.route("/institutions/<page_name>")
@courses.route("/instituciones/<page_name>")
def institutions(page_name):
    return render_template("/courses/institutions/{}.html".format(page_name.replace('-','_')))

@courses.route("/games/<page_name>")
@courses.route("/juegos/<page_name>")
def games(page_name):
    return render_template("/courses/games/{}.html".format(page_name.replace('-','_')))


@courses.route("/dashboard")
def dashboard():
    modules = Module.objects().all()
    return render_template("/courses/dashboard.html", modules=modules)

# View for a course module
@courses.route("/module")
def module():
    module_id = request.args.get("module_id")

    module = Module.objects(id=module_id).first()
    if module is None:
        print("[DEBUG]: Module not found, id: {}".format(module_id))
        return redirect(url_for("courses.dashboard"))

    return render_template("courses/module.html", module=module)

@courses.route("/task")
@login_required
def task():
    module_id = request.args.get("module_id")
    task_num  = int(request.args.get("task_num"))
    
    if module_id is None or \
        task_num is None or \
        task_num < 0:
        return redirect(url_for("courses.dashboard"))

    module = Module.objects(id=module_id).first()
    if module is None or \
        task_num >= len(module.tasks):
        return redirect(url_for("courses.dashboard"))
    
    task = None
    try:
        task = module.tasks[task_num]
    except IndexError:
        pass

    if task is None:
        return redirect(url_for("courses.dashboard"))
    

    form = None
    if task._cls == "MultipleChoiceQuiz":
        form = MultipleChoiceQuizForm.from_mongo_obj(task)

    

    return render_template("courses/task.html", form=form)