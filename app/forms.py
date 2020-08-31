import re
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, Email, ValidationError

from app import Message

data_required = InputRequired(Message.UserRegistration.ERROR_REQUIRED_FIELD)


class LoginForm(FlaskForm):
    email = StringField("Correo", validators=[data_required, Email(M)])
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

    _special_characters_raw = R"""!#$%&()*+-/:;<=>?@[\]^{|}~"""
    _special_characters = tuple(_special_characters_raw)
    
    # TODO: Change password validation to a more maintable version that allows specific messages.
    def validate_password(self, field):
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
            raise ValidationError(Message.UserRegistration.ERROR_PASSWORD_LENGTH)
        
        # Max length: 64
        if len(password) > 64:
            validation = False
            raise ValidationError(Message.UserRegistration.ERROR_PASSWORD_LENGTH)
        
        # At least one number
        if not any(char.isdigit() for char in password):
            validation = False
            raise ValidationError(Message.UserRegistration.ERROR_PASSWORD_AT_LEAST_ONE_NUMBER)

        # At least one upper case letter
        if not any(char.isupper() for char in password):
            validation = False
            raise ValidationError(Message.UserRegistration.ERROR_PASSWORD_AT_LEAST_ONE_UPPERCASE)

        # At least one lower case letter
        if not any(char.islower() for char in password):
            validation = False
            raise ValidationError(Message.UserRegistration.ERROR_PASSWORD_AT_LEAST_ONE_LOWERCASE)

        # At least one special symbol (list between double quotes): "!#$%&()*+-/:;<=>?@[\]^{|}~"
        if not any(char in RegisterForm._special_characters for char in password):
            validation = False
            raise ValidationError(Message.UserRegistration.ERROR_PASSWORD_AT_LEAST_ONE_SPECIAL_CHARACTER.format(RegisterForm._special_characters_raw))

        return validation
        
        