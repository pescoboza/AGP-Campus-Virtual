from flask import redirect, render_template, url_for, request
from flask_login import login_required

from . import courses
from ..models import Module
from .forms import MultipleChoiceQuizForm

@courses.route("/")
def empty():
    return redirect(url_for("courses.dashboard"))

@courses.route("/dashboard")
def dashboard():
    modules = Module.objects().all()
    return render_template("/courses/dashboard.html", modules=modules)

# View for a course module
@courses.route("/module")
@login_required
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