from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required

from app import Msg
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ResetPasswordResetForm
from ..models import User, generate_password_hash

@auth.route("/login",methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(email=form.email.data)
        if user is None:
            print("[DEBUG]: User not found: {}".format(form.email.data))
            flash(Msg.Flash.INVALID_CREDENTIALS)
            return redirect(url_for("auth.login"))
        
        if not user.check_password(form.password.data):
            print("[DEBUG]: Invalid user credentials: {} {}".format(form.email.data, form.password.data))
            flash(Msg.Flash.INVALID_CREDENTIALS)
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
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

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash(Msg.Flash.LOGOUT_USER)
    return redirect(url_for("main.index"))


@auth.route("/change-password", methods=["GET", "POST"])
@fresh_login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        
        # Check the old password
        if current_user.check_password(form.old_password.data):
        
            # Check that new password is not the same as the old one
            if form.old_password.data == form.password.data:
                flash(Msg.Flash.SAME_AS_OLD_PASSWORD)
                print("[DEBUG]: User {} tried to change to same password.".format(current_user.email))
                return redirect(url_for("auth.change_password"))

        else:
            flash(Msg.Flash.INVALID_OLD_PASSWORD)
            print("[DEBUG]: Password change request, incorrect old password. User: {}".format(current_user.email))
            return redirect(url_for("auth.change_password"))

        
        # Check that the user curently signed in is still on the database
        user = User.get_user(email=current_user.email)
        if user is None:
            print("[DEBUG]: Password change request, user not found: {}".format(current_user.email))
            return redirect(url_for("error.not_found"))

        # No errors, proceed to commit changes to database
        user.password_hash = generate_password_hash(form.password.data)
        user.save()
        print("[DEBUG]: Password change from user {}.".format(user.email))
        flash(Msg.Flash.PASSWORD_CHANGE_SUCCESFUL)
        return redirect(url_for("main.index"))
    return render_template("auth/change_password.html", form=form)

@auth.route("recover-password", methods=["GET", "POST"])
@auth.route("reset", methods=["GET", "POST"])
def recover_password():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.get_user(email=form.email.data)
        flash(Msg.Flash.RECOVERY_REQUEST)
        if user is not None:
            # Send confirmation email
            pass