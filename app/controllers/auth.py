from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Vérification si l'utilisateur est déjà connecté et redirection vers la page de résumé
    if current_user.is_authenticated:
        return redirect(url_for('resume.view_resume'))
    
    form = RegistrationForm()
    if form.validate_on_submit():  # Validation du formulaire lors de la soumission
        # Création d'un nouvel utilisateur avec les données du formulaire
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data , 
            last_name=form.last_name.data
        )
        # Hachage et stockage du mot de passe
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Enregistrement réussi ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Vérification si l'utilisateur est déjà connecté et redirection vers la page de résumé
    if current_user.is_authenticated:
        return redirect(url_for('resume.view_resume'))
    
    form = LoginForm()
    if form.validate_on_submit():  # Validation du formulaire lors de la soumission
        # Recherche de l'utilisateur en fonction de l'email
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # Vérification du mot de passe
            login_user(user, remember=form.remember.data)  # Connexion de l'utilisateur
            next_page = request.args.get('next')  # Récupération de la page suivante à rediriger
            return redirect(next_page or url_for('resume.view_resume'))  # Redirection vers la page de résumé ou la page suivante
        else:
            flash('Échec de la connexion. Veuillez vérifier votre email et votre mot de passe.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    # Déconnexion de l'utilisateur
    logout_user()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('auth.login'))  # Redirection vers la page de connexion
