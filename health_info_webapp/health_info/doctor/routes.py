from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import Doctor, Users, DiseaseType, Specialize
from health_info.doctor.forms import DoctorForm, SpecializeForm
from health_info.doctor import doctor
from sqlalchemy.exc import IntegrityError

@doctor.route('/doctors')
def list_doctors():
    doctors = Doctor.query.all()
    return render_template('doctor/list.html', doctors=doctors)

@doctor.route('/doctors/new', methods=['GET', 'POST'])
def new_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.query.get(email)
        if not user:
            # flash('User with this email does not exist. Please create the user first.', 'danger')
            return redirect(url_for('users.new_user'))
        existing_doctor = Doctor.query.get(email)
        if existing_doctor:
            # flash('Doctor with this email already exists.', 'warning')
            return redirect(url_for('doctor.list_doctors'))
        doctor_entry = Doctor(
            email=email,
            degree=form.degree.data
        )
        try:
            db.session.add(doctor_entry)
            db.session.commit()
            # flash('New doctor has been added!', 'success')
            return redirect(url_for('doctor.list_doctors'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while adding the doctor.', 'danger')
    return render_template('doctor/create_doctor.html', form=form, legend='New Doctor')

@doctor.route('/doctors/<email>/update', methods=['GET', 'POST'])
def update_doctor(email):
    doctor_entry = Doctor.query.get_or_404(email)
    form = DoctorForm()
    if form.validate_on_submit():
        if form.email.data != doctor_entry.email:
            # flash('Email cannot be changed.', 'warning')
            return redirect(url_for('doctor.update_doctor', email=email))
        doctor_entry.degree = form.degree.data
        try:
            db.session.commit()
            # flash('Doctor has been updated!', 'success')
            return redirect(url_for('doctor.list_doctors'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while updating the doctor.', 'danger')
    elif request.method == 'GET':
        form.email.data = doctor_entry.email
        form.degree.data = doctor_entry.degree
    return render_template('doctor/create_doctor.html', form=form, legend='Update Doctor')

@doctor.route('/doctors/<email>/delete', methods=['POST'])
def delete_doctor(email):
    doctor_entry = Doctor.query.get_or_404(email)
    try:
        db.session.delete(doctor_entry)
        db.session.commit()
        # flash('Doctor has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        # flash('An error occurred while deleting the doctor.', 'danger')
    return redirect(url_for('doctor.list_doctors'))

@doctor.route('/doctors/<email>/specializations', methods=['GET', 'POST'])
def manage_specializations(email):
    doctor_entry = Doctor.query.get_or_404(email)
    form = SpecializeForm()
    if form.validate_on_submit():
        disease_type_id = form.disease_type_id.data
        disease_type = DiseaseType.query.get(disease_type_id)
        if not disease_type:
            # flash('Disease Type ID does not exist.', 'danger')
            return redirect(url_for('doctor.manage_specializations', email=email))
        existing_specialization = Specialize.query.filter_by(email=email, id=disease_type_id).first()
        if existing_specialization:
            # flash('This specialization already exists.', 'warning')
            return redirect(url_for('doctor.manage_specializations', email=email))
        specialization = Specialize(
            email=email,
            id=disease_type_id
        )
        try:
            db.session.add(specialization)
            db.session.commit()
            # flash('Specialization added!', 'success')
            return redirect(url_for('doctor.manage_specializations', email=email))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while adding the specialization.', 'danger')
    specializations = Specialize.query.filter_by(email=email).all()
    return render_template('doctor/specializations.html', doctor=doctor_entry, form=form, specializations=specializations)