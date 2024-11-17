from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import Record, PublicServant, Country, Disease
from health_info.record.forms import RecordForm
from health_info.record import record
from sqlalchemy.exc import IntegrityError

@record.route('/records')
def list_records():
    records = Record.query.all()
    return render_template('record/list.html', records=records)

@record.route('/records/new', methods=['GET', 'POST'])
def new_record():
    form = RecordForm()
    if form.validate_on_submit():
        email = form.email.data
        cname = form.cname.data
        disease_code = form.disease_code.data

        # Validate foreign keys
        public_servant = PublicServant.query.get(email)
        if not public_servant:
            # flash('Public Servant does not exist. Please create the public servant first.', 'danger')
            return redirect(url_for('public_servant.new_public_servant'))

        country = Country.query.get(cname)
        if not country:
            # flash('Country does not exist. Please create the country first.', 'danger')
            return redirect(url_for('country.new_country'))  # Assuming you have a country module

        disease = Disease.query.get(disease_code)
        if not disease:
            # flash('Disease does not exist. Please create the disease first.', 'danger')
            return redirect(url_for('disease.new_disease'))

        # Check if record already exists
        existing_record = Record.query.filter_by(email=email, cname=cname, disease_code=disease_code).first()
        if existing_record:
            # flash('This record already exists.', 'warning')
            return redirect(url_for('record.list_records'))

        record_entry = Record(
            email=email,
            cname=cname,
            disease_code=disease_code,
            total_deaths=form.total_deaths.data,
            total_patients=form.total_patients.data
        )
        try:
            db.session.add(record_entry)
            db.session.commit()
            # flash('New record has been added!', 'success')
            return redirect(url_for('record.list_records'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while adding the record.', 'danger')
    return render_template('record/create_record.html', form=form, legend='New Record')

@record.route('/records/<email>/<cname>/<disease_code>/update', methods=['GET', 'POST'])
def update_record(email, cname, disease_code):
    record_entry = Record.query.get_or_404((email, cname, disease_code))
    form = RecordForm()
    if form.validate_on_submit():
        if (form.email.data != record_entry.email or
            form.cname.data != record_entry.cname or
            form.disease_code.data != record_entry.disease_code):
            # flash('Primary keys cannot be changed.', 'warning')
            return redirect(url_for('record.update_record', email=email, cname=cname, disease_code=disease_code))

        record_entry.total_deaths = form.total_deaths.data
        record_entry.total_patients = form.total_patients.data
        try:
            db.session.commit()
            # flash('Record has been updated!', 'success')
            return redirect(url_for('record.list_records'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while updating the record.', 'danger')
    elif request.method == 'GET':
        form.email.data = record_entry.email
        form.cname.data = record_entry.cname
        form.disease_code.data = record_entry.disease_code
        form.total_deaths.data = record_entry.total_deaths
        form.total_patients.data = record_entry.total_patients
    return render_template('record/create_record.html', form=form, legend='Update Record')

@record.route('/records/<email>/<cname>/<disease_code>/delete', methods=['POST'])
def delete_record(email, cname, disease_code):
    record_entry = Record.query.get_or_404((email, cname, disease_code))
    try:
        db.session.delete(record_entry)
        db.session.commit()
        # flash('Record has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        # flash('An error occurred while deleting the record.', 'danger')
    return redirect(url_for('record.list_records'))