from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User
from . import auth
from .forms import EditUser, CallLog, LogIn
from datetime import datetime


@auth.route('/')
@login_required
def index():
    return redirect(url_for('magazines.all_magazines'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LogIn()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('magazines.all_magazines'))

        flash('Either your username or password are incorrect.')
    return render_template('form.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.login'))


@auth.route('/add/user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = EditUser()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            user = User(email=form.email.data,
                        password=form.password.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        role=form.role.data,
                        name='{} {}'.format(form.first_name.data, form.last_name.data))

            db.session.add(user)
            db.session.commit()
            flash('User sucessfully added.')

            return redirect(url_for('.all_users'))

        else:
            flash('That user already exists.')

    return render_template('form.html', form=form)


@auth.route('/edit/user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get(id)

    if user is not None:
        form = EditUser(obj=user)

        if form.validate_on_submit():
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.name='{} {}'.format(form.first_name.data, form.last_name.data)

            if form.password.data and form.confirm.data:
                user.password = form.password.data
                db.session.commit()

            db.session.commit()
            flash('User successfully edited.')
            return redirect(url_for('.user', id=id))

        return render_template('form.html', form=form)

    flash('That user does not exist.')
    return redirect(url_for('.all_users'))


@auth.route('/archive/user/<int:id>')
@login_required
def archive_user(id):
    user = User.query.get(id)

    if user:
        user.active = False

        tasks = Task.query.filter_by(employee=user)

        if tasks:
            for task in tasks:
                task.assigned_to = None
                db.session.commit()

        db.session.commit()
        flash('The user has been archived and all of their tasks have been unassigned.')
        return redirect(url_for('.all_users'))

    flash('No such user exists.')
    return redirect(url_for('.all_users'))


@auth.route('/delete/user/<int:id>')
@login_required
def delete_user(id):
    user = User.query.get(id)

    if user:

        tasks = Task.query.filter_by(employee=user)

        if tasks:
            for task in tasks:
                task.assigned_to = None
                db.session.commit()

        db.session.delete(user)
        db.session.commit()
        flash('The user has been deleted and all of their tasks have been unassigned.')
        return redirect(url_for('.all_users'))

    flash('No such user exists.')
    return redirect(url_for('.all_users'))


@auth.route('/users')
@login_required
def all_users():
    users = User.query.all()

    return render_template('all_users.html', users=users)


@auth.route('/user/<int:id>')
@login_required
def user(id):
    user = User.query.get(id)

    if not user:
        flash('That user does not exist.')
        return redirect(url_for('.all_users'))

    return render_template('user.html', user=user)


@auth.route('/call_log', methods=['GET', 'POST'])
@login_required
def call_log():
    form = CallLog()

    if form.validate_on_submit():
        call = Call(company=form.company.data,
                    person=form.person.data,
                    notes=form.notes.data,
                    called_date=datetime.utcnow)

        db.session.add(call)
        db.session.commit(call)

    return render_template('form.html', form=form)


@auth.route('/test')
@login_required
def test():
    test = current_user.get_id()

    return render_template('test.html', test=test)