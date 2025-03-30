from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, URL


class ProfileForm(FlaskForm):
    # Champ obligatoire avec une longueur minimale et maximale
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=2, max=64)])

    # Vérification du format d'email
    email = StringField('Adresse email', validators=[DataRequired(), Email()])

    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Nom de famille', validators=[DataRequired(), Length(max=20)])

    # Champ optionnel avec une contrainte de longueur maximale
    phone = StringField('Numéro de téléphone', validators=[Optional(), Length(max=20)])
    address = StringField('Adresse', validators=[Optional(), Length(max=200)])

    bio = TextAreaField('À propos de moi', validators=[Optional()])

    # Champ de fichier avec restriction aux formats jpg, png et jpeg
    profile_image = FileField('Image de profil', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Seulement des images !')])

    # Champs d'URL avec validation de format et longueur maximale
    website = StringField('Site web', validators=[Optional(), URL(), Length(max=100)])
    linkedin = StringField('LinkedIn', validators=[Optional(), URL(), Length(max=100)])
    github = StringField('GitHub', validators=[Optional(), URL(), Length(max=100)])
    twitter = StringField('Twitter', validators=[Optional(), URL(), Length(max=100)])

    submit = SubmitField('Mettre à jour')  # Bouton de soumission du formulaire
