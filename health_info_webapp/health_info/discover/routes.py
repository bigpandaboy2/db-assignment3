from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import Discover, Country, Disease
from health_info.discover.forms import DiscoverForm
from health_info.discover import discover
from sqlalchemy.exc import IntegrityError

@discover.route('/discoveries')
def list_discoveries():
    discoveries = Discover.query.all()
    return render_template('discover/list.html', discoveries=discoveries)

@discover.route('/discoveries/new', methods=['GET', 'POST'])
def new_discovery():
    form = DiscoverForm()
    if form.validate_on_submit():
        cname = form.cname.data
        disease_code = form.disease_code.data

        # Validate foreign keys
        country = Country.query.get(cname)
        if not country:
            # flash('Country does not exist. Please create the country first.', 'danger')
            return redirect(url_for('country.new_country'))  # Assuming you have a country module

        disease = Disease.query.get(disease_code)
        if not disease:
            # flash('Disease does not exist. Please create the disease first.', 'danger')
            return redirect(url_for('disease.new_disease'))

        # Check if discovery already exists
        existing_discovery = Discover.query.filter_by(cname=cname, disease_code=disease_code).first()
        if existing_discovery:
            # flash('This discovery already exists.', 'warning')
            return redirect(url_for('discover.list_discoveries'))

        discovery_entry = Discover(
            cname=cname,
            disease_code=disease_code,
            first_enc_date=form.first_enc_date.data
        )
        try:
            db.session.add(discovery_entry)
            db.session.commit()
            # flash('New discovery has been added!', 'success')
            return redirect(url_for('discover.list_discoveries'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while adding the discovery.', 'danger')
    return render_template('discover/create_discover.html', form=form, legend='New Discovery')

@discover.route('/discoveries/<cname>/<disease_code>/update', methods=['GET', 'POST'])
def update_discovery(cname, disease_code):
    discovery_entry = Discover.query.get_or_404((cname, disease_code))
    form = DiscoverForm()
    if form.validate_on_submit():
        if (form.cname.data != discovery_entry.cname or
            form.disease_code.data != discovery_entry.disease_code):
            # flash('Country Name and Disease Code cannot be changed.', 'warning')
            return redirect(url_for('discover.update_discovery', cname=cname, disease_code=disease_code))

        discovery_entry.first_enc_date = form.first_enc_date.data
        try:
            db.session.commit()
            # flash('Discovery has been updated!', 'success')
            return redirect(url_for('discover.list_discoveries'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while updating the discovery.', 'danger')
    elif request.method == 'GET':
        form.cname.data = discovery_entry.cname
        form.disease_code.data = discovery_entry.disease_code
        form.first_enc_date.data = discovery_entry.first_enc_date
    return render_template('discover/create_discover.html', form=form, legend='Update Discovery')

@discover.route('/discoveries/<cname>/<disease_code>/delete', methods=['POST'])
def delete_discovery(cname, disease_code):
    discovery_entry = Discover.query.get_or_404((cname, disease_code))
    try:
        db.session.delete(discovery_entry)
        db.session.commit()
        # flash('Discovery has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        # flash('An error occurred while deleting the discovery.', 'danger')
    return redirect(url_for('discover.list_discoveries'))