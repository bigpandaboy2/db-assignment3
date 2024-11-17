from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import Country
from health_info.country.forms import CountryForm
from health_info.country import country
from sqlalchemy.exc import IntegrityError

@country.route('/countries')
def list_countries():
    countries = Country.query.all()
    return render_template('country/list.html', countries=countries)

@country.route('/countries/new', methods=['GET', 'POST'])
def new_country():
    form = CountryForm()
    if form.validate_on_submit():
        cname = form.cname.data
        existing_country = Country.query.get(cname)
        if existing_country:
            # flash('Country with this name already exists.', 'warning')
            return redirect(url_for('country.list_countries'))
        country_entry = Country(
            cname=cname,
            population=form.population.data
        )
        try:
            db.session.add(country_entry)
            db.session.commit()
            # flash('New country has been added!', 'success')
            return redirect(url_for('country.list_countries'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while adding the country.', 'danger')
    return render_template('country/create_country.html', form=form, legend='New Country')

@country.route('/countries/<cname>/update', methods=['GET', 'POST'])
def update_country(cname):
    country_entry = Country.query.get_or_404(cname)
    form = CountryForm()
    if form.validate_on_submit():
        if form.cname.data != country_entry.cname:
            # flash('Country name cannot be changed.', 'warning')
            return redirect(url_for('country.update_country', cname=cname))
        country_entry.population = form.population.data
        try:
            db.session.commit()
            # flash('Country has been updated!', 'success')
            return redirect(url_for('country.list_countries'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while updating the country.', 'danger')
    elif request.method == 'GET':
        form.cname.data = country_entry.cname
        form.population.data = country_entry.population
    return render_template('country/create_country.html', form=form, legend='Update Country')

@country.route('/countries/<cname>/delete', methods=['POST'])
def delete_country(cname):
    country_entry = Country.query.get_or_404(cname)
    try:
        db.session.delete(country_entry)
        db.session.commit()
        # flash('Country has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        # flash('An error occurred while deleting the country.', 'danger')
    return redirect(url_for('country.list_countries'))
