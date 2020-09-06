from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, EqualTo, Length, Email, ValidationError

from .. import Msg
from ..models import user_occupations, user_genders

data_required = InputRequired(Msg.UserRegistration.ERROR_REQUIRED_FIELD)

# Password validator function for all forms in which a new password is created.
def validate_password(field):
        """
            Password constraints:
            - At least one number
            - At least one upper case letter
            - At least one lower case letter
            - At least one special symbol (list between double quotes): "!#$%&()*+-/:;<=>?@[\]^{|}~"
            - Length between 6 and 64 characters long
        """ 
        password = field.data
        validation = True
        
        # Min length: 8
        if len(password) < 8:
            validation = False
            raise ValidationError(Msg.UserRegistration.ERROR_PASSWORD_LENGTH)
        
        # Max length: 64
        if len(password) > 64:
            validation = False
            raise ValidationError(Msg.UserRegistration.ERROR_PASSWORD_LENGTH)
        
        # At least one number
        if not any(char.isdigit() for char in password):
            validation = False
            raise ValidationError(Msg.UserRegistration.ERROR_PASSWORD_AT_LEAST_ONE_NUMBER)

        # At least one upper case letter
        if not any(char.isupper() for char in password):
            validation = False
            raise ValidationError(Msg.UserRegistration.ERROR_PASSWORD_AT_LEAST_ONE_UPPERCASE)

        # At least one lower case letter
        if not any(char.islower() for char in password):
            validation = False
            raise ValidationError(Msg.UserRegistration.ERROR_PASSWORD_AT_LEAST_ONE_LOWERCASE)

        # At least one special symbol (list between double quotes): "!#$%&()*+-/:;<=>?@[\]^{|}~"
        if not any(char in RegisterForm._special_characters for char in password):
            validation = False
            raise ValidationError(Msg.UserRegistration.ERROR_PASSWORD_AT_LEAST_ONE_SPECIAL_CHARACTER.format(RegisterForm._special_characters_raw))

        return validation



class LoginForm(FlaskForm):
    email = StringField("Correo", validators=[data_required, Email(Msg.UserRegistration.ERROR_INVALID_EMAIL)])
    password = PasswordField("Contraseña", validators=[data_required])
    remember_me = BooleanField("Mantener mi sesión iniciada")
    submit = SubmitField("Iniciar sesión")

class RegisterForm(FlaskForm):
    email = StringField("Correo", validators=[data_required, Email(Msg.UserRegistration.ERROR_INVALID_EMAIL)])
    first_name = StringField("Nombre", validators=[data_required])
    paternal_last_name = StringField("Apellido paterno", validators=[data_required])
    maternal_last_name = StringField("Apellido materno", validators=[data_required])
    birth_date = DateField("Fecha de nacimiento", validators=[data_required])
    gender = SelectField("Género", choices=user_genders, validators=[data_required])
    occupation = SelectField("Ocupación",choices=user_occupations, validators=[data_required])

    password = PasswordField("Contraseña", validators=[data_required, EqualTo("confirm_password", message=Msg.UserRegistration.ERROR_PASSWORD_MATCH)])
    confirm_password = PasswordField("Confirmar contraseña", validators=[data_required])

    accept_terms_and_conditions = BooleanField(Msg.UserRegistration.ACCEPT_TERMS, validators=[InputRequired(message=Msg.UserRegistration.ERROR_ACCEPT_TERMS)])
    submit = SubmitField("Registrarse")

    _special_characters_raw = R"""!#$%&()*+-/:;<=>?@[\]^{|}~"""
    _special_characters = tuple(_special_characters_raw)
    
    def validate_password(self, field):
        return validate_password(field)

# Form for changing a new password when the old one is known.
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Antigua contraseña", validators=[data_required])
    password = PasswordField("Contraseña", validators=[data_required, EqualTo("confirm_password", message=Msg.UserRegistration.ERROR_PASSWORD_MATCH)])
    confirm_password = PasswordField("Confirmar contraseña", validators=[data_required])

    submit = SubmitField("Modficar contraseña")

# Form to request email to reset password.
class PasswordResetRequestForm(FlaskForm):
    email = StringField("Correo", validators=[data_required, Email(Msg.UserRegistration.ERROR_INVALID_EMAIL)])

    submit = SubmitField("Enviar")

# Form to change password from lost passwrod email request.
class PasswordResetForm(FlaskForm):
    password = PasswordField("Nueva ontraseña", validators=[data_required, EqualTo("confirm_password", message=Msg.UserRegistration.ERROR_PASSWORD_MATCH)])
    confirm_password = PasswordField("Confirmar contraseña", validators=[data_required])
    
    submit = SubmitField("Reestablecer contraseña")
    
    def validate_password(self, field):
        return validate_password(field)