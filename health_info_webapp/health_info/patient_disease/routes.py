from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import PatientDisease, Patients, Disease
from health_info.patient_disease.forms import PatientDiseaseForm
from health_info.patient_disease import patient_disease
from sqlalchemy.exc import IntegrityError

@patient_disease.route('/patient_diseases')
def list_patient_diseases():
    patient_diseases = PatientDisease.query.all()
    return render_template('patient_disease/list.html', patient_diseases=patient_diseases)

@patient_disease.route('/patient_diseases/new', methods=['GET', 'POST'])
def new_patient_disease():
    form = PatientDiseaseForm()
    if form.validate_on_submit():
        email = form.email.data
        disease_code = form.disease_code.data

        # Validate foreign keys
        patient = Patients.query.get(email)
        if not patient:
            # flash('Patient does not exist. Please create the patient first.', 'danger')
            return redirect(url_for('patients.new_patient'))

        disease = Disease.query.get(disease_code)
        if not disease:
            # flash('Disease does not exist. Please create the disease first.', 'danger')
            return redirect(url_for('disease.new_disease'))

        # Check if patient disease record already exists
        existing_patient_disease = PatientDisease.query.filter_by(email=email, disease_code=disease_code).first()
        if existing_patient_disease:
            # flash('This patient disease record already exists.', 'warning')
            return redirect(url_for('patient_disease.list_patient_diseases'))

        patient_disease_entry = PatientDisease(
            email=email,
            disease_code=disease_code,
        )
        try:
            db.session.add(patient_disease_entry)
            db.session.commit()
            # flash('New patient disease record has been added!', 'success')
            return redirect(url_for('patient_disease.list_patient_diseases'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while adding the patient disease record.', 'danger')
    return render_template('patient_disease/create_patient_disease.html', form=form, legend='New Patient Disease')

@patient_disease.route('/patient_diseases/<email>/<disease_code>/update', methods=['GET', 'POST'])
def update_patient_disease(email, disease_code):
    patient_disease_entry = PatientDisease.query.get_or_404((email, disease_code))
    form = PatientDiseaseForm()
    if form.validate_on_submit():
        if form.email.data != patient_disease_entry.email or form.disease_code.data != patient_disease_entry.disease_code:
            # flash('Patient Email and Disease Code cannot be changed.', 'warning')
            return redirect(url_for('patient_disease.update_patient_disease', email=email, disease_code=disease_code))

        try:
            db.session.commit()
            # flash('Patient disease record has been updated!', 'success')
            return redirect(url_for('patient_disease.list_patient_diseases'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while updating the patient disease record.', 'danger')
    elif request.method == 'GET':
        form.email.data = patient_disease_entry.email
        form.disease_code.data = patient_disease_entry.disease_code
    return render_template('patient_disease/create_patient_disease.html', form=form, legend='Update Patient Disease')

@patient_disease.route('/patient_diseases/<email>/<disease_code>/delete', methods=['POST'])
def delete_patient_disease(email, disease_code):
    patient_disease_entry = PatientDisease.query.get_or_404((email, disease_code))
    try:
        db.session.delete(patient_disease_entry)
        db.session.commit()
        # flash('Patient disease record has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        # flash('An error occurred while deleting the patient disease record.', 'danger')
    return redirect(url_for('patient_disease.list_patient_diseases'))