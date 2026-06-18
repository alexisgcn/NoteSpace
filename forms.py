# forms.py
# Formularios para NoteSpace (Flask-WTF)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# ---------------- REGISTRO ----------------
class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=6, message="Mínimo 6 caracteres")
    ])
    confirm = PasswordField('Confirmar contraseña', validators=[
        DataRequired(),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Registrarse')


# ---------------- LOGIN ----------------
class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')


# ---------------- NOTAS ----------------
class NoteForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Contenido')
    tags = StringField('Etiquetas (separadas por coma)')
    submit = SubmitField('Guardar')
