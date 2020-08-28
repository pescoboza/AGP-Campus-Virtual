from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user

from app import app
from app.forms import LoginForm
from app.models import User


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    # TODO: Add database integration.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            # TODO: Add better flashed messages.
            flash("Usuario o contraseña inválidos.")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)
        return redirect("/index")
    
    return render_template("login.html", title="Iniciar sesión", form=form)