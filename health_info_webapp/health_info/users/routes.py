from flask import render_template, url_for, flash, redirect, request
from health_info import db
from health_info.models import Users
from health_info.users.forms import UserForm
from health_info.users import users

@users.route('/users')
def list_users():
    users_list = Users.query.all()
    return render_template('users/list.html', users=users_list)

@users.route('/users/new', methods=['GET', 'POST'])
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        user = Users(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            salary=form.salary.data,
            phone=form.phone.data,
            cname=form.cname.data
        )
        db.session.add(user)
        db.session.commit()
        # flash('New user has been created!', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('users/create_user.html', form=form, legend='New User')

@users.route('/users/<email>/update', methods=['GET', 'POST'])
def update_user(email):
    user = Users.query.get_or_404(email)
    form = UserForm()
    if form.validate_on_submit():
        new_email = form.email.data
        if new_email != user.email:
            # Check if new email already exists
            existing_user = Users.query.get(new_email)
            if existing_user:
                # flash('A user with the new email already exists.', 'warning')
                return redirect(url_for('users.update_user', email=email))
            # Update the email
            user.email = new_email
        # Update other fields
        user.name = form.name.data
        user.surname = form.surname.data
        user.salary = form.salary.data
        user.phone = form.phone.data
        user.cname = form.cname.data
        try:
            db.session.commit()
            # flash('User information has been updated!', 'success')
            return redirect(url_for('users.list_users'))
        except Exception as e:
            db.session.rollback()
            # flash('An error occurred while updating the user: {}'.format(e), 'danger')
            return redirect(url_for('users.update_user', email=email))
    elif request.method == 'GET':
        form.email.data = user.email
        form.name.data = user.name
        form.surname.data = user.surname
        form.salary.data = user.salary
        form.phone.data = user.phone
        form.cname.data = user.cname
    return render_template('users/create_user.html', form=form, legend='Update User')


@users.route('/users/<email>/delete', methods=['POST'])
def delete_user(email):
    user = Users.query.get_or_404(email)
    db.session.delete(user)
    db.session.commit()
    # flash('User has been deleted!', 'success')
    return redirect(url_for('users.list_users'))