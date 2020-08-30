from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, Email

from app import Message

data_required = InputRequired(Message.UserRegistration.ERROR_REQUIRED_FIELD)


class LoginForm(FlaskForm):
    email = StringField("Correo", validators=[data_required])
    password = PasswordField("Contraseña", validators=[data_required])
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Iniciar sesión")

class RegisterForm(FlaskForm):
    email = StringField("Correo", validators=[data_required])
    first_name = StringField("Nombre", validators=[data_required])
    last_name = StringField("Apellidos", validators=[data_required])
    password = PasswordField("Contraseña", validators=[data_required, EqualTo("confirm_password", message=Message.UserRegistration.ERROR_PASSWORD_MATCH)])
    confirm_password = PasswordField("Repetir contraseña", validators=[data_required])

    accept_terms_and_conditions = BooleanField(Message.UserRegistration.ACCEPT_TERMS, validators=[InputRequired(message=Message.UserRegistration.ERROR_ACCEPT_TERMS)])
    submit = SubmitField("Registrarse")