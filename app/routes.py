from flask import flash, redirect, render_template

from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    # TODO: Add database integration.
    form = LoginForm()
    if form.validate_on_submit():
        #flash("DEBUG: Login request for user {}.".format(form.username.data))
        return redirect("/index")
    return render_template("login.html", title="Iniciar sesión", form=form)