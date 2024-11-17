from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import Specialize, DiseaseType, Doctor
from health_info.specialize.forms import SpecializeForm
from health_info.specialize import specialize
from sqlalchemy.exc import IntegrityError

@specialize.route('/specialize')
def list_specializations():
    specializations = Specialize.query.all()
    return render_template('specialize/list.html', specializations=specializations)

@specialize.route('/specialize/new', methods=['GET', 'POST'])
def new_specialization():
    form = SpecializeForm()
    if form.validate_on_submit():
        id = form.id.data
        email = form.email.data

        disease_type = DiseaseType.query.get(id)
        if not disease_type:
            return redirect(url_for('disease_type.new_disease_type'))  

        doctor = Doctor.query.get(email)
        if not doctor:
            return redirect(url_for('doctor.new_doctor')) 

        existing_specialization = Specialize.query.filter_by(id=id, email=email).first()
        if existing_specialization:
            return redirect(url_for('specialize.list_specializations'))

        specialization_entry = Specialize(
            id=id,
            email=email
        )
        try:
            db.session.add(specialization_entry)
            db.session.commit()
            return redirect(url_for('specialize.list_specializations'))
        except IntegrityError:
            db.session.rollback()
    return render_template('specialize/create_specialization.html', form=form, legend='New Specialization')

@specialize.route('/specialize/<int:id>/<email>/update', methods=['GET', 'POST'])
def update_specialization(id, email):
    specialization_entry = Specialize.query.get_or_404((id, email))
    form = SpecializeForm()

    if form.validate_on_submit():
        new_id = form.id.data
        new_email = form.email.data

        if new_id != id or new_email != email:
            try:
                db.session.delete(specialization_entry)
                db.session.commit() 

                new_specialization = Specialize(id=new_id, email=new_email)
                db.session.add(new_specialization)
                db.session.commit()
                return redirect(url_for('specialize.list_specializations'))
            except IntegrityError:
                db.session.rollback()
                # flash('Error updating specialization. Ensure the new values are valid and unique.', 'danger')
                return redirect(url_for('specialize.update_specialization', id=id, email=email))

        specialization_entry.id = new_id
        specialization_entry.email = new_email
        try:
            db.session.commit()
            # flash('Specialization updated successfully!', 'success')
            return redirect(url_for('specialize.list_specializations'))
        except IntegrityError:
            db.session.rollback()
            # flash('Error updating specialization. Please try again.', 'danger')

    elif request.method == 'GET':
        form.id.data = specialization_entry.id
        form.email.data = specialization_entry.email

    return render_template('specialize/create_specialization.html', form=form, legend='Update Specialization')

@specialize.route('/specialize/<int:id>/<email>/delete', methods=['POST'])
def delete_specialization(id, email):
    specialization_entry = Specialize.query.get_or_404((id, email))
    try:
        db.session.delete(specialization_entry)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return redirect(url_for('specialize.list_specializations'))