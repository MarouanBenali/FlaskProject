from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.forms.profile import ProfileForm
import os
import uuid
from werkzeug.datastructures import FileStorage  


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

def save_picture(form_picture):
    """Enregistrer l'image du profil avec un nom de fichier unique"""
    if not isinstance(form_picture, FileStorage):  
        return None  

    random_hex = uuid.uuid4().hex  # Génère un identifiant unique pour éviter les collisions de noms de fichiers
    _, f_ext = os.path.splitext(form_picture.filename)  # Récupère l'extension du fichier pour la conserver
    picture_filename = random_hex + f_ext  # Crée le nom de fichier final
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_filename)  # Détermine le chemin de stockage

    form_picture.save(picture_path)  # Sauvegarde l'image
    return picture_filename

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)  # Charge le formulaire avec les données actuelles de l'utilisateur
    
    if form.validate_on_submit():  # Valide le formulaire au moment de la soumission
        if form.profile_image.data and isinstance(form.profile_image.data, FileStorage):  # Vérifie si une image est téléchargée
            picture_file = save_picture(form.profile_image.data)  # Enregistre l'image et récupère son nom de fichier
            if picture_file:
                current_user.profile_image = picture_file  # Met à jour l'image de profil de l'utilisateur
        
        # Met à jour les autres informations du profil
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.bio = form.bio.data
        current_user.website = form.website.data
        current_user.linkedin = form.linkedin.data
        current_user.github = form.github.data
        current_user.twitter = form.twitter.data
        
        db.session.commit()  # Sauvegarde les modifications dans la base de données
        flash('Profil mis à jour avec succès!', 'success')  # Affiche un message de succès
        return redirect(url_for('profile.profile'))  # Redirige vers la page de profil mise à jour
    
    return render_template('profile/edit.html', form=form)

@profile_bp.route('/view')
@login_required
def view_profile():
    return render_template('profile/view.html')
