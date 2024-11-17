from flask import Blueprint, render_template, url_for, redirect, request
from health_info import db
from health_info.models import Users, Patients
from health_info.patients.forms import PatientForm
from sqlalchemy.exc import IntegrityError

patients = Blueprint('patients', __name__)

@patients.route('/patients')
def list_patients():
    patients_list = Patients.query.all()
    return render_template('patients/list.html', patients=patients_list)

@patients.route('/patients/new', methods=['GET', 'POST'])
def new_patient():
    form = PatientForm()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.query.get(email)
        if not user:
            # Redirect to create a new user
            return redirect(url_for('users.new_user'))
        existing_patient = Patients.query.get(email)
        if existing_patient:
            return redirect(url_for('patients.list_patients'))
        patient = Patients(email=email)
        try:
            db.session.add(patient)
            db.session.commit()
            # flash('New patient has been added!', 'success')  # Removed
            return redirect(url_for('patients.list_patients'))
        except IntegrityError as e:
            db.session.rollback()
            # Handle the error as needed
    return render_template('patients/create_patient.html', form=form, legend='New Patient')

@patients.route('/patients/<email>/update', methods=['GET', 'POST'])
def update_patient(email):
    patient = Patients.query.get_or_404(email)
    form = PatientForm()
    if form.validate_on_submit():
        new_email = form.email.data
        if new_email != patient.email:
            existing_patient = Patients.query.get(new_email)
            if existing_patient:
                return redirect(url_for('patients.update_patient', email=email))
            user = Users.query.get(new_email)
            if not user:
                return redirect(url_for('users.new_user'))
            try:
                patient.email = new_email
                db.session.commit()
                # flash('Patient email has been updated!', 'success')  # Removed
                return redirect(url_for('patients.list_patients'))
            except Exception as e:
                db.session.rollback()
                # Handle the error as needed
        else:
            return redirect(url_for('patients.list_patients'))
    elif request.method == 'GET':
        form.email.data = patient.email
    return render_template('patients/create_patient.html', form=form, legend='Update Patient')

@patients.route('/patients/<email>/delete', methods=['POST'])
def delete_patient(email):
    patient = Patients.query.get_or_404(email)
    try:
        db.session.delete(patient)
        db.session.commit()
        # flash('Patient has been deleted!', 'success')  # Removed
    except IntegrityError as e:
        db.session.rollback()
        # Handle the error as needed
    return redirect(url_for('patients.list_patients'))