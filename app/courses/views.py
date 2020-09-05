from flask import redirect, render_template, url_for
from flask_login import login_required

from . import courses
from ..models import Module

@courses.route("/dashboad")
def dashboard():
    return render_template("/courses/dashboard.html")

# View for a course module
@courses.route("/<module_id>")
@login_required
def module(module_id):
    module = Module.objects(id=module_id).first()
    if module is None:
        print("[DEBUG]: Module not found, id: {}".format(module_id))
        return redirect(url_for("main.index"))

    render_template("courses/module.html", module=module)
