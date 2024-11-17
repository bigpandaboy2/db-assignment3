from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import DiseaseType
from health_info.disease_type.forms import DiseaseTypeForm
from health_info.disease_type import disease_type
from sqlalchemy.exc import IntegrityError

@disease_type.route('/disease_types')
def list_disease_types():
    disease_types = DiseaseType.query.all()
    return render_template('disease_type/list.html', disease_types=disease_types)

@disease_type.route('/disease_types/new', methods=['GET', 'POST'])
def new_disease_type():
    form = DiseaseTypeForm()
    if form.validate_on_submit():
        id = form.id.data
        existing_type = DiseaseType.query.get(id)
        if existing_type:
            # flash('Disease Type with this ID already exists.', 'warning')
            return redirect(url_for('disease_type.list_disease_types'))
        disease_type_entry = DiseaseType(
            id=id,
            description=form.description.data
        )
        try:
            db.session.add(disease_type_entry)
            db.session.commit()
            # flash('New disease type has been added!', 'success')
            return redirect(url_for('disease_type.list_disease_types'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while adding the disease type.', 'danger')
    return render_template('disease_type/create_disease_type.html', form=form, legend='New Disease Type')

@disease_type.route('/disease_types/<int:id>/update', methods=['GET', 'POST'])
def update_disease_type(id):
    disease_type_entry = DiseaseType.query.get_or_404(id)
    form = DiseaseTypeForm()
    if form.validate_on_submit():
        if form.id.data != disease_type_entry.id:
            # flash('ID cannot be changed.', 'warning')
            return redirect(url_for('disease_type.update_disease_type', id=id))
        disease_type_entry.description = form.description.data
        try:
            db.session.commit()
            # flash('Disease type has been updated!', 'success')
            return redirect(url_for('disease_type.list_disease_types'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while updating the disease type.', 'danger')
    elif request.method == 'GET':
        form.id.data = disease_type_entry.id
        form.description.data = disease_type_entry.description
    return render_template('disease_type/create_disease_type.html', form=form, legend='Update Disease Type')

@disease_type.route('/disease_types/<int:id>/delete', methods=['POST'])
def delete_disease_type(id):
    disease_type_entry = DiseaseType.query.get_or_404(id)
    try:
        db.session.delete(disease_type_entry)
        db.session.commit()
        # flash('Disease type has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        # flash('An error occurred while deleting the disease type. It may be referenced by diseases.', 'danger')
    return redirect(url_for('disease_type.list_disease_types'))
