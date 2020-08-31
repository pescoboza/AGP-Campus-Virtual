from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import Msg
from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User

@auth.route("/login",methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # NOTE: Remember to unpack form fields with form.field.data.
        user = User.objects(email=form.email.data).first()

        if user is None:
            print("[DEBUG]: User not found: {}".format(form.email.data))
            flash(Msg.Flash.INVALID_CREDENTIALS)
            return redirect(url_for("auth.login"))
        
        if not user.check_password(form.password.data):
            print("[DEBUG]: Invalid user credentials: {} {}".format(form.email.data, form.password.data))
            flash(Msg.Flash.INVALID_CREDENTIALS)
            return redirect(url_for("auth.login"))

        if login_user(user, remember=form.remember_me.data):
            print("[DEBUG]: Login from user: {} {}".format(user.email, user.first_name))
        return redirect(url_for("main.index"))
    
    return render_template("auth/login.html", title="Iniciar sesión", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.get_user(form.email.data) is not None:
            print("[DEBUG]: User with email {} already registered.".format(form.email.data))
            flash(Msg.UserRegistration.ERROR_EMAIL_IN_USE)
            return redirect(url_for("auth.register"))

        new_user = User.create_new_user(email=form.email.data, 
                            first_name=form.first_name.data, 
                            last_name=form.last_name.data, 
                            password=form.password.data)
        new_user.save()
        login_user(new_user, remember=False)
        flash(Msg.Flash.NEW_USER.format(first_name=new_user.first_name))
        return redirect(url_for("main.index"))
    
    return render_template("auth/register.html", title="Registrarse", form=form)

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    flash(Msg.Flash.LOGOUT_USER)
    return redirect(url_for("main.index"))