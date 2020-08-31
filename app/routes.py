from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import app, Message
from app.forms import LoginForm, RegisterForm
from app.models import User


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# TODO: Add user registration.
@app.route("/login",methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # NOTE: Remember to unpack form fields with form.field.data.
        user = User.objects(email=form.email.data).first()

        if user is None:
            print("[DEBUG]: User not found: {}".format(form.email.data))
            flash(Message.Flash.INVALID_CREDENTIALS)
            return redirect(url_for("login"))
        
        if not user.check_password(form.password.data):
            print("[DEBUG]: Invalid user credentials: {} {}".format(form.email.data, form.password.data))
            flash(Message.Flash.INVALID_CREDENTIALS)
            return redirect(url_for("login"))

        if login_user(user, remember=form.remember_me.data):
            print("[DEBUG]: Login from user: {} {}".format(user.email, user.first_name))
        return redirect("/index")
    
    return render_template("login.html", title="Iniciar sesión", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.get_user(form.email.data) is not None:
            print("[DEBUG]: User with email {} already registered.".format(form.email.data))
            flash(Message.UserRegistration.ERROR_EMAIL_IN_USE)
            return redirect(url_for("register"))

        new_user = User.create_new_user(email=form.email.data, 
                            first_name=form.first_name.data, 
                            last_name=form.last_name.data, 
                            password=form.password.data)
        new_user.save()
        login_user(new_user, remember=False)
        flash(Message.Flash.NEW_USER.format(first_name=new_user.first_name))
        return redirect(url_for("index"))
    
    return render_template("register.html", title="Registrarse", form=form)

@login_required
@app.route("/logout")
def logout():
    logout_user()
    flash(Message.Flash.LOGOUT_USER)
    return redirect("/index")