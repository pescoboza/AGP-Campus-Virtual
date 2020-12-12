from flask import flash, redirect, request, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required

from app import Msg
from . import auth
from ..main import main # For user profile page
from .forms import *
from ..models import User, generate_password_hash, QUIZ_CODES
from ..email import send_email


@auth.route("/iniciar-sesion", methods=["GET", "POST"])
def login():

    # User is already logged in
    if not current_user.is_anonymous:
        flash(Msg.Flash.ALREADY_LOGGED_IN)
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_user(email=form.email.data)
        if user is None:
            # print("[DEBUG] User not found: {}".format(form.email.data))
            flash(Msg.Flash.INVALID_CREDENTIALS)
            return redirect(url_for("auth.login"))

        # Redirect user the page he or she was about to enter, but got asked to verify credentials.
        next = request.args.get("next")
        if next is None or not next.startswith('/'):
            next = url_for("main.index")

        if not user.check_password(form.password.data):
            # print("[DEBUG] Invalid user credentials: {} {}".format(
            #     form.email.data, form.password.data))
            flash(Msg.Flash.INVALID_CREDENTIALS)
            return redirect(url_for("auth.login", next=next))

        login_user(user, remember=form.remember_me.data)
        # print("[DEBUG] Login from user: {} {}".format(
        #     user.email, user.first_name))

        flash("Ha iniciado sesión correctamente.")
        return redirect(next)

    return render_template("auth/login.html", title="Iniciar sesión", form=form)


@auth.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.get_user(form.email.data) is not None:
            # print("[DEBUG] User with email {} already registered.".format(
            #     form.email.data))
            flash(Msg.UserRegistration.ERROR_EMAIL_IN_USE)
            return redirect(url_for("auth.registrarse"))

        new_user = \
            User\
            .create_new_user(email=form.email.data,
                             first_name=form.first_name.data,
                             paternal_last_name=form.paternal_last_name.data,
                             maternal_last_name=form.maternal_last_name.data,
                             birth_date=form.birth_date.data,
                             gender=form.gender.data,
                             occupation=form.occupation.data,
                             password=form.password.data)

        # print("[DEBUG] New user created. Showing JSON:")
        # print(new_user.to_json())
        # print("[DEBUG] New user EOF.")
        new_user.save()

        login_user(new_user, remember=False)
        flash(Msg.Flash.NEW_USER.format(first_name=new_user.first_name))
        return redirect(url_for("main.index"))

    return render_template("auth/registrarse.html", title="Registrarse", form=form)


@auth.route("/cerrar-sesion")
def logout():
    if not current_user.is_anonymous:
        logout_user()
        flash("Ha cerrado sesión exitosamente.")
    return redirect(url_for("main.index"))


@auth.route("/cambiar-contrasena", methods=["GET", "POST"])
@fresh_login_required
def cambiar_contrasena():
    form = ChangePasswordForm()
    if form.validate_on_submit():

        # Check the old password
        if current_user.check_password(form.old_password.data):

            # Check that new password is not the same as the old one
            if form.old_password.data == form.password.data:
                flash(Msg.Flash.SAME_AS_OLD_PASSWORD)
                # print("[DEBUG] User {} tried to change to same password.".format(
                #     current_user.email))
                return redirect(url_for("auth.cambiar_contrasena"))

        else:
            flash(Msg.Flash.INVALID_OLD_PASSWORD)
            # print("[DEBUG] Password change request, incorrect old password. User: {}".format(
            #     current_user.email))
            return redirect(url_for("auth.cambiar_contrasena"))

        # Check that the user curently signed in is still on the database
        user = User.get_user(email=current_user.email)
        if user is None:
            # print("[DEBUG] Password change request, user not found: {}".format(
            #     current_user.email))
            return redirect(url_for("error.not_found"))

        # No errors, proceed to commit changes to database
        user.password_hash = generate_password_hash(form.password.data)
        user.save()
        # print("[DEBUG] Password change from user {}.".format(user.email))
        flash(Msg.Flash.PASSWORD_CHANGE_SUCCESFUL)
        return redirect(url_for("main.index"))
    return render_template("auth/cambiar_contrasena.html", form=form)


# View to request a password change, arrived at through "forgot password?"
# Redirects to index if user is NOT anonymous
@auth.route("/reestablecer-contrasena", methods=["GET", "POST"])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))

    form = PasswordResetRequestForm()
    if form.validate_on_submit():

        user = User.get_user(form.email.data)
        if user:
            token = user.generate_reset_token()
            send_email(user.email, Msg.Mail.RESET_PASSWORD_SUBJECT, "auth/email/reset_password",
                       user=user, token=token)
        flash(Msg.Flash.PASSWORD_RESET_EMAIL_SENT)
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)


# View to change reset password after token sent to email is validated.
# Redirects to index if user is NOT anonymous
@auth.route("/reestablecer-contrasena/<token>", methods=["GET", "POST"])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))

    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            flash(Msg.Flash.PASSWORD_CHANGE_SUCCESFUL)
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("main.index"))
    return render_template("auth/reset_password.html", form=form)


@auth.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():

    # Get the user
    user = User.objects(email=current_user.email).first()
    if user is None:
        return redirect(url_for("main.index"))

    # Check if it's admin to include special options
    is_admin = user.has_perm("admin")

    # Create user data form
    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        data = form.data
        data.pop("submit")
        data.pop("csrf_token")

        is_save = False
        for k, v in data.items():
            if v != user[k]:
                is_save = True
                user[k] = v

        if is_save:
            user.save()
            flash("Su perfil ha sido actualizado.")
            return redirect(url_for("auth.perfil"))

    quiz_info = {}
    for qc in QUIZ_CODES:
        if qc == "diag":
            continue
        quiz_name = QUIZ_CODES[qc]["full_name"]
        score, max_score = user.quiz_data[qc]["score"]  # Unpack list of two items
        is_passed = user.quiz_data[qc]["is_passed"]
        is_obligatory = QUIZ_CODES[qc]["is_obligatory"]
        certificate_url = url_for("main.certificate", name=QUIZ_CODES[qc]["certificate_url"])

        quiz_info[quiz_name] = {
            "score": score,
            "max_score": max_score,
            "is_passed": is_passed,
            "is_obligatory": is_obligatory,
            "certificate_url": certificate_url
        }

    return render_template("auth/perfil.html", form=form, quiz_info=quiz_info, is_admin=is_admin)
