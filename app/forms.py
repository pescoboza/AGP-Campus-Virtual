from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

from app import Message

class FieldLength:
    DB_STRING = 64
    DB_HASH = 256

    FORM_EMAIL = DB_STRING

class LoginForm(FlaskForm):
    email = StringField("Correo", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Iniciar sesión")

class RegisterForm(FlaskForm):
    email = StringField("Correo", validators=[DataRequired()])
    first_name = StringField("Nombre", validators=[DataRequired()])
    last_name = StringField("Apellidos", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired(), EqualTo("confirm_password", message=Message.UserRegistration.ERROR_PASSWORD_MATCH)])
    confirm_password = PasswordField("Repetir contraseña", validators=[DataRequired()])

    accept_terms_and_conditions = BooleanField(Message.UserRegistration.ACCEPT_TERMS, validators=[DataRequired()])
    submit = SubmitField("Registrarse")