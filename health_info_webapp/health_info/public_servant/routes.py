from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import PublicServant, Users
from health_info.public_servant.forms import PublicServantForm
from health_info.public_servant import public_servant
from sqlalchemy.exc import IntegrityError

@public_servant.route('/public_servants')
def list_public_servants():
    public_servants = PublicServant.query.all()
    return render_template('public_servant/list.html', public_servants=public_servants)

@public_servant.route('/public_servants/new', methods=['GET', 'POST'])
def new_public_servant():
    form = PublicServantForm()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.query.get(email)
        if not user:
            # flash('User with this email does not exist. Please create the user first.', 'danger')
            return redirect(url_for('users.new_user'))
        existing_public_servant = PublicServant.query.get(email)
        if existing_public_servant:
            # flash('Public Servant with this email already exists.', 'warning')
            return redirect(url_for('public_servant.list_public_servants'))
        public_servant_entry = PublicServant(
            email=email,
            department=form.department.data
        )
        try:
            db.session.add(public_servant_entry)
            db.session.commit()
            # flash('New public servant has been added!', 'success')
            return redirect(url_for('public_servant.list_public_servants'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while adding the public servant.', 'danger')
    return render_template('public_servant/create_public_servant.html', form=form, legend='New Public Servant')

@public_servant.route('/public_servants/<email>/update', methods=['GET', 'POST'])
def update_public_servant(email):
    public_servant_entry = PublicServant.query.get_or_404(email)
    form = PublicServantForm()
    if form.validate_on_submit():
        if form.email.data != public_servant_entry.email:
            # flash('Email cannot be changed.', 'warning')
            return redirect(url_for('public_servant.update_public_servant', email=email))
        public_servant_entry.department = form.department.data
        try:
            db.session.commit()
            # flash('Public servant has been updated!', 'success')
            return redirect(url_for('public_servant.list_public_servants'))
        except IntegrityError:
            db.session.rollback()
            # flash('An error occurred while updating the public servant.', 'danger')
    elif request.method == 'GET':
        form.email.data = public_servant_entry.email
        form.department.data = public_servant_entry.department
    return render_template('public_servant/create_public_servant.html', form=form, legend='Update Public Servant')

@public_servant.route('/public_servants/<email>/delete', methods=['POST'])
def delete_public_servant(email):
    public_servant_entry = PublicServant.query.get_or_404(email)
    try:
        db.session.delete(public_servant_entry)
        db.session.commit()
        # flash('Public servant has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        # flash('An error occurred while deleting the public servant.', 'danger')
    return redirect(url_for('public_servant.list_public_servants'))