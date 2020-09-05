from flask_login import render_template
from flask_login import login_required

from . import courses

@courses.route("/dashboad")
@login_required
def dashboard():
    return render_template("/courses/dashboard.html")