from app import db
from datetime import datetime


# Modèle représentant une éducation d'un utilisateur
class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers l'utilisateur
    institution = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    field_of_study = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.Date, nullable=False)  # Date de début de l'éducation
    end_date = db.Column(db.Date, nullable=True)  # Date de fin de l'éducation (optionnelle)
    description = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref=db.backref('education', lazy=True, cascade="all, delete-orphan"))
    # Relation un-à-plusieurs avec l'utilisateur, la suppression en cascade est activée

# Modèle représentant l'expérience professionnelle d'un utilisateur
class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers l'utilisateur
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.Date, nullable=False)  # Date de début de l'expérience
    end_date = db.Column(db.Date, nullable=True)  # Date de fin de l'expérience (optionnelle)
    current = db.Column(db.Boolean, default=False)  # Indicateur si l'expérience est actuelle ou terminée
    description = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref=db.backref('experience', lazy=True, cascade="all, delete-orphan"))
    # Relation un-à-plusieurs avec l'utilisateur, la suppression en cascade est activée

# Modèle représentant une compétence d'un utilisateur
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers l'utilisateur
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=True)  # Niveau de la compétence, de 1 à 5
    user = db.relationship('User', backref=db.backref('skills', lazy=True, cascade="all, delete-orphan"))
    # Relation un-à-plusieurs avec l'utilisateur, la suppression en cascade est activée

# Modèle représentant un projet d'un utilisateur
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers l'utilisateur
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)  # Date de début du projet (optionnelle)
    end_date = db.Column(db.Date, nullable=True)  # Date de fin du projet (optionnelle)
    user = db.relationship('User', backref=db.backref('projects', lazy=True, cascade="all, delete-orphan"))
    # Relation un-à-plusieurs avec l'utilisateur, la suppression en cascade est activée

# Modèle représentant une langue maîtrisée par un utilisateur
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers l'utilisateur
    name = db.Column(db.String(50), nullable=False)
    proficiency = db.Column(db.String(20), nullable=True)  # Niveau de maîtrise, par exemple "Courant", "Intermédiaire", "Débutant"
    user = db.relationship('User', backref=db.backref('languages', lazy=True, cascade="all, delete-orphan"))
    # Relation un-à-plusieurs avec l'utilisateur, la suppression en cascade est activée

# Modèle représentant un CV d'un utilisateur
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers l'utilisateur
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création du CV
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Date de dernière mise à jour
    user = db.relationship('User', backref=db.backref('resume', uselist=False, cascade="all, delete-orphan"))
    # Relation un-à-un avec l'utilisateur, la suppression en cascade est activée et uselist=False empêche l'utilisation de plusieurs CV
