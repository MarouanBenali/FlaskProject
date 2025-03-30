
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# Modèle représentant un utilisateur
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)  # Nom d'utilisateur unique et obligatoire
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email unique et obligatoire
    password_hash = db.Column(db.String(128))  # Hash du mot de passe pour la sécurité
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)  # Biographie de l'utilisateur
    profile_image = db.Column(db.String(200), nullable=True)  # Image de profil de l'utilisateur
    website = db.Column(db.String(200), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    github = db.Column(db.String(200), nullable=True)
    twitter = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création du compte

    # Méthode pour définir le mot de passe de manière sécurisée (en le hachant)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Méthode pour vérifier si le mot de passe entré correspond au mot de passe haché
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Représentation de l'utilisateur sous forme de chaîne de caractères
    def __repr__(self):
        return f'<User {self.username}>'
