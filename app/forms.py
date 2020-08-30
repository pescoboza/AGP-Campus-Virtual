from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Correo", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Iniciar sesión")

class RegisterForm(FlaskForm):
    email = StringField("Correo", validators=[DataRequired()])
    first_name = StringField("Nombre", validators=[DataRequired()])
    last_name = StringField("Apellidos", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    repeat_password = PasswordField("Repetir contraseña", validators=[DataRequired()])

    accept_terms_and_conditions = BooleanField("He leído y acepto los términos y condiciones.", validators=[DataRequired()])
    submit = SubmitField("Registrarse")