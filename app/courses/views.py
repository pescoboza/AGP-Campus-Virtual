from flask_login import render_template
from flask_login import login_required

from . import courses

@courses.route("/dashboad")
def dashboard():
    return render_template("/courses/dashboard.html")

@courses.route("/<course_id>")
@login_required
def take_course(course_id):
    

