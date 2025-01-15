from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from models import User


class ProfileForm(FlaskForm):
    # Campo Nombre
    nombre = StringField(
        'Nombre', 
        validators=[DataRequired(message="El nombre es requerido")]
    )
    
    # Campo Email
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message="El email es requerido")
        ]
    )
    
    # Campo Géneros Preferidos
    generos_preferidos = StringField(
        'Géneros Preferidos (Ingréselos separados por comas)',
        validators=[DataRequired(message="Por favor ingrese sus géneros preferidos")]
    )
    
    # Campo Películas Favoritas
    peliculas_favoritas = StringField(
        'Películas Favoritas (Ingréselas separadas por comas)',
        validators=[DataRequired(message="Por favor ingrese sus películas favoritas")]
    )
    
    # Campo Directores Favoritos
    directores_favoritos = StringField(
        'Directores Favoritos (Ingréselos separados por comas)',
        validators=[DataRequired(message="Por favor ingrese sus directores favoritos")]
    )
    
    submit = SubmitField('Guardar')



class SignUpForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(message='Esto no parece ser un correo válido')], )
    nombre = StringField('Nombre', validators=[DataRequired(message='Este campo es obligatorio')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Este campo es obligatorio')])
    password_confirmation = PasswordField(
        'Confirmar Contraseña',
        validators=[
            DataRequired(message='Este campo es obligatorio'),
            EqualTo('password', message='Las contraseñas deben coincidir')
        ]
    )
    submit = SubmitField('Registrarse')
    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()  # Consulta en la base de datos
        if existing_user:
            raise ValidationError("El correo electrónico ya está registrado.")


class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(message='Esto no parece ser un correo válido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Este campo es obligatorio')])
    submit = SubmitField('Iniciar Sesión')