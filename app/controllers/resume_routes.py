from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.resume_models import Resume, Education, Experience, Skill, Project, Language
from app.forms.resume_forms import ResumeForm, EducationForm, ExperienceForm, SkillForm, ProjectForm, LanguageForm
from datetime import datetime

# Création du Blueprint pour le module 'resume'
resume_bp = Blueprint('resume', __name__, url_prefix='/resume')

# Route pour afficher le CV de l'utilisateur
@resume_bp.route('/')
@login_required
def view_resume():
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    if not resume:
        flash('Aucun CV créé. Créez-en un maintenant.', 'info')
        return redirect(url_for('resume.create_resume'))
    
    # Récupération des informations supplémentaires pour le CV
    education = Education.query.filter_by(user_id=current_user.id).all()
    experience = Experience.query.filter_by(user_id=current_user.id).all()
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    projects = Project.query.filter_by(user_id=current_user.id).all()
    languages = Language.query.filter_by(user_id=current_user.id).all()
    
    return render_template('resume/view.html', 
                          resume=resume, 
                          education=education,
                          experience=experience,
                          skills=skills,
                          projects=projects,
                          languages=languages)

# Route pour créer un nouveau CV
@resume_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_resume():
    # Vérifier si un CV existe déjà
    existing_resume = Resume.query.filter_by(user_id=current_user.id).first()
    if existing_resume:
        return redirect(url_for('resume.edit_resume'))
    
    form = ResumeForm()
    if form.validate_on_submit():
        # Création du CV
        resume = Resume(
            user_id=current_user.id,
            title=form.title.data,
            summary=form.summary.data
        )
        db.session.add(resume)
        db.session.commit()
        flash('CV créé avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/edit.html', form=form, is_new=True)

# Route pour éditer un CV existant
@resume_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_resume():
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    if not resume:
        return redirect(url_for('resume.create_resume'))
    
    form = ResumeForm(obj=resume)
    if form.validate_on_submit():
        # Mise à jour du CV
        form.populate_obj(resume)
        resume.updated_at = datetime.utcnow()
        db.session.commit()
        flash('CV mis à jour avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/edit.html', form=form, is_new=False)

# Route pour imprimer le CV
@resume_bp.route('/print')
@login_required
def print_resume():
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    if not resume:
        flash('Aucun CV créé. Créez-en un maintenant.', 'info')
        return redirect(url_for('resume.create_resume'))
    
    # Récupération des informations supplémentaires pour le CV
    education = Education.query.filter_by(user_id=current_user.id).all()
    experience = Experience.query.filter_by(user_id=current_user.id).all()
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    projects = Project.query.filter_by(user_id=current_user.id).all()
    languages = Language.query.filter_by(user_id=current_user.id).all()
    
    return render_template('resume/print.html', 
                          resume=resume, 
                          education=education,
                          experience=experience,
                          skills=skills,
                          projects=projects,
                          languages=languages)

# Routes pour l'éducation
@resume_bp.route('/education/add', methods=['GET', 'POST'])
@login_required
def add_education():
    form = EducationForm()
    if form.validate_on_submit():
        # Ajout d'une nouvelle éducation
        education = Education(
            user_id=current_user.id,
            institution=form.institution.data,
            degree=form.degree.data,
            field_of_study=form.field_of_study.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data
        )
        db.session.add(education)
        db.session.commit()
        flash('Éducation ajoutée avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/education_form.html', form=form, is_edit=False)

# Route pour éditer une éducation existante
@resume_bp.route('/education/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_education(id):
    education = Education.query.get_or_404(id)
    if education.user_id != current_user.id:
        abort(403)
    
    form = EducationForm(obj=education)
    if form.validate_on_submit():
        # Mise à jour de l'éducation
        form.populate_obj(education)
        db.session.commit()
        flash('Éducation mise à jour avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/education_form.html', form=form, is_edit=True)

# Route pour supprimer une éducation
@resume_bp.route('/education/delete/<int:id>', methods=['POST'])
@login_required
def delete_education(id):
    education = Education.query.get_or_404(id)
    if education.user_id != current_user.id:
        abort(403)
    
    db.session.delete(education)
    db.session.commit()
    flash('Éducation supprimée avec succès!', 'success')
    return redirect(url_for('resume.view_resume'))

# Routes pour l'expérience
@resume_bp.route('/experience/add', methods=['GET', 'POST'])
@login_required
def add_experience():
    form = ExperienceForm()
    if form.validate_on_submit():
        # Ajout d'une nouvelle expérience
        experience = Experience(
            user_id=current_user.id,
            company=form.company.data,
            position=form.position.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=None if form.current.data else form.end_date.data,
            current=form.current.data,
            description=form.description.data
        )
        db.session.add(experience)
        db.session.commit()
        flash('Expérience ajoutée avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/experience_form.html', form=form, is_edit=False)

# Route pour éditer une expérience existante
@resume_bp.route('/experience/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_experience(id):
    experience = Experience.query.get_or_404(id)
    if experience.user_id != current_user.id:
        abort(403)
    
    form = ExperienceForm(obj=experience)
    if form.validate_on_submit():
        # Mise à jour de l'expérience
        form.populate_obj(experience)
        if form.current.data:
            experience.end_date = None
        db.session.commit()
        flash('Expérience mise à jour avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/experience_form.html', form=form, is_edit=True)

# Route pour supprimer une expérience
@resume_bp.route('/experience/delete/<int:id>', methods=['POST'])
@login_required
def delete_experience(id):
    experience = Experience.query.get_or_404(id)
    if experience.user_id != current_user.id:
        abort(403)
    
    db.session.delete(experience)
    db.session.commit()
    flash('Expérience supprimée avec succès!', 'success')
    return redirect(url_for('resume.view_resume'))

# Routes pour les compétences
@resume_bp.route('/skill/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    form = SkillForm()
    if form.validate_on_submit():
        # Ajout d'une nouvelle compétence
        skill = Skill(
            user_id=current_user.id,
            name=form.name.data,
            level=form.level.data
        )
        db.session.add(skill)
        db.session.commit()
        flash('Compétence ajoutée avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/skill_form.html', form=form, is_edit=False)

# Route pour éditer une compétence existante
@resume_bp.route('/skill/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    if skill.user_id != current_user.id:
        abort(403)
    
    form = SkillForm(obj=skill)
    if form.validate_on_submit():
        # Mise à jour de la compétence
        form.populate_obj(skill)
        db.session.commit()
        flash('Compétence mise à jour avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/skill_form.html', form=form, is_edit=True)

# Route pour supprimer une compétence
@resume_bp.route('/skill/delete/<int:id>', methods=['POST'])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    if skill.user_id != current_user.id:
        abort(403)
    
    db.session.delete(skill)
    db.session.commit()
    flash('Compétence supprimée avec succès!', 'success')
    return redirect(url_for('resume.view_resume'))

# Routes pour les projets
@resume_bp.route('/project/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        # Ajout d'un nouveau projet
        project = Project(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            url=form.url.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Projet ajouté avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/project_form.html', form=form, is_edit=False)

# Route pour éditer un projet existant
@resume_bp.route('/project/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if project.user_id != current_user.id:
        abort(403)
    
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        # Mise à jour du projet
        form.populate_obj(project)
        db.session.commit()
        flash('Projet mis à jour avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/project_form.html', form=form, is_edit=True)

# Route pour supprimer un projet
@resume_bp.route('/project/delete/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if project.user_id != current_user.id:
        abort(403)
    
    db.session.delete(project)
    db.session.commit()
    flash('Projet supprimé avec succès!', 'success')
    return redirect(url_for('resume.view_resume'))

# Routes pour les langues
@resume_bp.route('/language/add', methods=['GET', 'POST'])
@login_required
def add_language():
    form = LanguageForm()
    if form.validate_on_submit():
        # Ajout d'une nouvelle langue
        language = Language(
            user_id=current_user.id,
            name=form.name.data,
            proficiency=form.proficiency.data
        )
        db.session.add(language)
        db.session.commit()
        flash('Langue ajoutée avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/language_form.html', form=form, is_edit=False)

# Route pour éditer une langue existante
@resume_bp.route('/language/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_language(id):
    language = Language.query.get_or_404(id)
    if language.user_id != current_user.id:
        abort(403)
    
    form = LanguageForm(obj=language)
    if form.validate_on_submit():
        # Mise à jour de la langue
        form.populate_obj(language)
        db.session.commit()
        flash('Langue mise à jour avec succès!', 'success')
        return redirect(url_for('resume.view_resume'))
    
    return render_template('resume/language_form.html', form=form, is_edit=True)

# Route pour supprimer une langue
@resume_bp.route('/language/delete/<int:id>', methods=['POST'])
@login_required
def delete_language(id):
    language = Language.query.get_or_404(id)
    if language.user_id != current_user.id:
        abort(403)
    
    db.session.delete(language)
    db.session.commit()
    flash('Langue supprimée avec succès!', 'success')
    return redirect(url_for('resume.view_resume'))
