from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User

class RegistrationForm(FlaskForm):
    # Champs pour l'inscription avec des validations
    first_name = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=25)])
    last_name = StringField('Nom de famille', validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('User_name', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Adresse email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6, max=10)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password'), Length(min=6, max=10)])
    submit = SubmitField('S\'inscrire')
    
    # Vérification de l'unicité du nom d'utilisateur
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
    
    # Vérification de l'unicité de l'email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Cet e-mail est déjà utilisé. Veuillez en utiliser un autre.")

class LoginForm(FlaskForm):
    # Champs pour la connexion avec des validations
    email = StringField('Adresse email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6, max=10)])
    remember = BooleanField('Rester connecté')
    submit = SubmitField('Se connecter')
