# Importation des modules nécessaires
from app import create_app, db
from app.models.user import User
from app.models.resume_models import Resume, Education, Experience, Skill, Project, Language
from datetime import datetime
from flask import render_template

# Création de l'application Flask
app = create_app()

# Contexte de l'application : Ajoute la date et l'heure actuelles au contexte de chaque requête
@app.context_processor
def inject_now():
    # Cette fonction renvoie l'heure actuelle en UTC à chaque template rendu
    return {'now': datetime.utcnow()}

# Contexte pour l'accès rapide aux objets dans le shell Flask
@app.shell_context_processor
def make_shell_context():
    # Renvoie un dictionnaire avec les objets de la base de données pour un accès rapide dans le shell interactif
    return {
        'db': db, 
        'User': User, 
        'Resume': Resume, 
        'Education': Education, 
        'Experience': Experience, 
        'Skill': Skill, 
        'Project': Project, 
        'Language': Language
    }

# Route de la page d'accueil
@app.route('/')
def home():
    # Affiche le template 'home.html' pour la page d'accueil
    return render_template('home.html')

# Exécution de l'application Flask
if __name__ == '__main__':
    # Lance l'application en mode débogage
    app.run(debug=True)
