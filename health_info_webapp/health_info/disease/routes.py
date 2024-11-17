from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import Disease, DiseaseType
from health_info.disease.forms import DiseaseForm
from health_info.disease import disease
from sqlalchemy.exc import IntegrityError

@disease.route('/diseases')
def list_diseases():
    diseases = Disease.query.all()
    return render_template('disease/list.html', diseases=diseases)

@disease.route('/diseases/new', methods=['GET', 'POST'])
def new_disease():
    form = DiseaseForm()
    if form.validate_on_submit():
        disease_code = form.disease_code.data
        existing_disease = Disease.query.get(disease_code)
        if existing_disease:
            #flash('A disease with this code already exists.', 'warning')
            return redirect(url_for('disease.list_diseases'))
        disease_type = DiseaseType.query.get(form.disease_type_id.data)
        if not disease_type:
            #flash('Disease Type ID does not exist. Please create the disease type first.', 'danger')
            return redirect(url_for('disease.new_disease_type'))
        disease = Disease(
            disease_code=disease_code,
            pathogen=form.pathogen.data,
            description=form.description.data,
            id=form.disease_type_id.data
        )
        try:
            db.session.add(disease)
            db.session.commit()
            #flash('New disease has been added!', 'success')
            return redirect(url_for('disease.list_diseases'))
        except IntegrityError:
            db.session.rollback()
            #flash('An error occurred while adding the disease.', 'danger')
    return render_template('disease/create_disease.html', form=form, legend='New Disease')

@disease.route('/diseases/<disease_code>/update', methods=['GET', 'POST'])
def update_disease(disease_code):
    disease = Disease.query.get_or_404(disease_code)
    form = DiseaseForm()
    if form.validate_on_submit():
        if form.disease_code.data != disease.disease_code:
            #flash('Disease code cannot be changed.', 'warning')
            return redirect(url_for('disease.update_disease', disease_code=disease_code))
        disease_type = DiseaseType.query.get(form.disease_type_id.data)
        if not disease_type:
            #flash('Disease Type ID does not exist.', 'danger')
            return redirect(url_for('disease.update_disease', disease_code=disease_code))
        disease.pathogen = form.pathogen.data
        disease.description = form.description.data
        disease.id = form.disease_type_id.data
        try:
            db.session.commit()
            #flash('Disease has been updated!', 'success')
            return redirect(url_for('disease.list_diseases'))
        except IntegrityError:
            db.session.rollback()
            #flash('An error occurred while updating the disease.', 'danger')
    elif request.method == 'GET':
        form.disease_code.data = disease.disease_code
        form.pathogen.data = disease.pathogen
        form.description.data = disease.description
        form.disease_type_id.data = disease.id
    return render_template('disease/create_disease.html', form=form, legend='Update Disease')

@disease.route('/diseases/<disease_code>/delete', methods=['POST'])
def delete_disease(disease_code):
    disease = Disease.query.get_or_404(disease_code)
    try:
        db.session.delete(disease)
        db.session.commit()
        #flash('Disease has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        #flash('An error occurred while deleting the disease.', 'danger')
    return redirect(url_for('disease.list_diseases'))