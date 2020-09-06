from flask import redirect, render_template, url_for, request
from flask_login import login_required

from . import courses
from ..models import Module

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
