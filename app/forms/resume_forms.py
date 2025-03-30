from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, URL, Length

class ResumeForm(FlaskForm):
    title = StringField('Titre du CV', validators=[DataRequired(), Length(max=100)])  # Champ obligatoire avec une longueur maximale
    summary = TextAreaField('Résumé', validators=[Optional(), Length(max=500)])  # Champ optionnel avec une longueur maximale
    submit = SubmitField('Sauvegarder')  # Bouton de soumission du formulaire

class EducationForm(FlaskForm):
    institution = StringField('Établissement', validators=[DataRequired(), Length(max=100)])
    degree = StringField('Diplôme', validators=[DataRequired(), Length(max=100)])
    field_of_study = StringField('Domaine d\'études', validators=[Optional(), Length(max=100)])
    
    # Champ Date avec un format spécifique, validation obligatoire
    start_date = DateField('Date de début', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('Date de fin', validators=[Optional()], format='%Y-%m-%d')  # Date optionnelle
    
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Sauvegarder')

class ExperienceForm(FlaskForm):
    company = StringField('Entreprise', validators=[DataRequired(), Length(max=100)])
    position = StringField('Poste', validators=[DataRequired(), Length(max=100)])
    location = StringField('Lieu', validators=[Optional(), Length(max=100)])
    
    # Validation des dates de début et de fin avec un format spécifique
    start_date = DateField('Date de début', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('Date de fin', validators=[Optional()], format='%Y-%m-%d')  # Date de fin optionnelle
    
    # Champ booléen pour savoir si l'utilisateur est actuellement employé
    current = BooleanField('Actuellement employé', default=False)
    
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Sauvegarder')

class SkillForm(FlaskForm):
    name = StringField('Compétence', validators=[DataRequired(), Length(max=50)])
    
    # Sélection d'un niveau avec un choix de valeurs prédéfinies
    level = SelectField('Niveau', choices=[(1, 'Débutant'), (2, 'Intermédiaire'), (3, 'Bon'), (4, 'Avancé'), (5, 'Expert')], coerce=int, validators=[Optional()])
    
    submit = SubmitField('Sauvegarder')

class ProjectForm(FlaskForm):
    title = StringField('Titre du projet', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    
    # URL avec validation de format
    url = StringField('URL du projet', validators=[Optional(), URL(), Length(max=200)])
    
    start_date = DateField('Date de début', validators=[Optional()], format='%Y-%m-%d')
    end_date = DateField('Date de fin', validators=[Optional()], format='%Y-%m-%d')
    
    submit = SubmitField('Sauvegarder')

class LanguageForm(FlaskForm):
    name = StringField('Langue', validators=[DataRequired(), Length(max=50)])
    
    # Sélection d'un niveau de compétence avec un choix prédéfini
    proficiency = SelectField('Niveau de compétence', choices=[('Débutant', 'Débutant'), ('Intermédiaire', 'Intermédiaire'), ('Bon', 'Bon'), ('Avancé', 'Avancé'), ('Fluent', 'Fluent')], validators=[DataRequired()])
    
    submit = SubmitField('Sauvegarder')
