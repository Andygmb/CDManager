from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Client, Contact, Magazine, Page, Task, Comment, Call
from . import main
from .forms import EditUser, EditClient, EditMag, EditTask, EditContact, CallLog, LogIn
from datetime import datetime
from sendgrid import SendGridError, SendGridClientError, SendGridServerError
import os
import sendgrid

sg = sendgrid.SendGridClient(os.environ.get('SENDGRIDUSER'),
                             os.environ.get('SENDGRIDPASS'), raise_errors=True)


def send_email(to, subject, text, sender, html=None):
    message = sendgrid.Mail()
    message.add_to(to)
    message.set_subject(subject)
    message.set_text(text)
    message.set_from(sender)

    if html:
        message.set_html(html)

    try:
        sg.send(message)
    except SendGridClientError:
        flash('There was a problem sending the email.')
        return redirect(url_for('.all_tasks'))
    except SendGridServerError:
        flash('There was a problem sending the email.')
        return redirect(url_for('.all_tasks'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LogIn()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('.all_magazines'))

        flash('Either your username or password are incorrect.')
    return render_template('form.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.login'))


@main.route('/add/user', methods=['GET', 'POST'])
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


@main.route('/add/client', methods=['GET', 'POST'])
@login_required
def add_client():
    form = EditClient()

    if form.validate_on_submit():
        client = Client.query.filter_by(name=form.name.data).first()

        if client is None:
            client = Client(name=form.name.data,
                            address=form.address.data,
                            note=form.note.data)

            db.session.add(client)
            db.session.commit()
            flash('Client successfully added.')
            return redirect(url_for('.all_clients'))

        else:
            flash('{} already exists.'.format(str(client)))

    return render_template('form.html', form=form)


@main.route('/<int:client_id>/add/contact', methods=['GET', 'POST'])
@login_required
def add_contact(client_id):
    form = EditContact()

    client = Client.query.get(client_id)

    if form.validate_on_submit():
        contact = Contact(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          name='{} {}'.format(form.first_name.data, form.last_name.data),
                          position=form.position.data,
                          main_email=form.main_email.data,
                          main_phone=form.main_phone.data,
                          company=client)

        if form.secondary_email.data:
            contact.secondary_email=form.secondary_email.data
        if form.secondary_phone.data:
            contact.secondary_phone=form.secondary_phone.data

        db.session.add(contact)
        db.session.commit()

        return redirect(url_for('.client', id=client.id))

    return render_template('form.html', form=form)


@main.route('/add/magazine', methods=['GET', 'POST'])
@login_required
def add_magazine():
    form = EditMag()

    if form.validate_on_submit():
        mag = Magazine(name=form.name.data,
                       owner=form.owner.data,
                       sales_person=form.sales_person.data,
                       page_count=form.page_count.data,
                       client_mag='{} - {}'.format(form.owner.data, form.name.data),
                       note=form.note.data)

        db.session.add(mag)
        db.session.commit()

        id = mag.id

        count = 1

        while count < form.page_count.data + 1:
            page = Page(number=count, magazine_id=id)
            db.session.add(page)
            db.session.commit()
            count += 1

        flash('Magazine successfully added.')
        return redirect(url_for('.all_magazines'))

    return render_template('form.html', form=form)


@main.route('/<int:mag>/add/task', methods=['GET', 'POST'])
@login_required
def add_task(mag):

    mag = Magazine.query.get(mag)

    if mag:

        form = EditTask()
        form.pages.query = mag.pages
        
        if form.validate_on_submit():

            task = Task(name=form.name.data,
                        description=form.description.data,
                        create_date=datetime.utcnow(),
                        status=form.status.data,
                        users=form.users.data,
                        assigned_by=current_user.get_id(),
                        pages=form.pages.data,
                        magazine=mag)

            if form.due_date.data:
                task.due_date=form.due_date.data

            db.session.add(task)
            db.session.commit()

            if task.status == 'road-blocked':
                assigner = User.query.get(task.assigner.id)

                send_email(assigner.email, "One of your tasks is road blocked.",
                           "{} - {}".format(task.name, task.description), task.employee.email)

            elif task.status == 'inactive' or task.status == 'finished':
                task.active = False
                db.session.commit()

            else:
                task.active = True

                for user in task.users:
                    send_email(user.email, "You've been assigned a new task.",
                            """{}
                            Task: {}
                            Description: {}
                            Due Date: {}
                            Assigned by: {}""".format(mag.client_mag, task.name, task.description, task.due_date, task.assigned_by), 
                            task.assigner.email)
                db.session.commit()

            for task in mag.tasks:
                if task.status == 'road-blocked':
                    mag.status = 'road-blocked'
                    db.session.commit()
                    break
            else:
                mag.status = 'active'
                db.session.commit()

            if form.comment.data:
                user = User.query.get(current_user.get_id())

                comment = Comment(posted_date=datetime.utcnow(),
                                  text=form.comment.data,
                                  poster=user,
                                  task=task)

                db.session.add(comment)
                db.session.commit()

            flash('Task successfully added.')
            return redirect(url_for('.magazine', id=mag.id))

        return render_template('form.html', form=form)

    flash('That magazine does not exist.')
    return render_template(url_for(all_magazines))


@main.route('/edit/user/<int:id>', methods=['GET', 'POST'])
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


@main.route('/edit/client/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    client = Client.query.get(id)

    if client is not None:
        form = EditClient(obj=client)

        if form.validate_on_submit():
            client.name = form.name.data
            client.phone = form.phone.data
            client.address = form.address.data
            client.note = form.note.data

            db.session.add(client)
            db.session.commit()
            flash('Client successfully edited.')
            return redirect(url_for('.client', id=id))



        return render_template('form.html', form=form)

    flash('That client does not exist.')
    return redirect(url_for('.all_clients'))


@main.route('/edit/contact/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    contact = Contact.query.get(id)

    if contact is not None:
        form = EditContact(obj=contact)

        if form.validate_on_submit():
            contact.first_name = form.first_name.data
            contact.last_name = form.last_name.data
            contact.name = '{} {}'.format(form.first_name.data, form.last_name.data)
            contact.main_email = form.main_email.data
            contact.main_phone = form.main_phone.data

            if form.secondary_phone.data:
                contact.secondary_phone = form.secondary_phone.data

            if form.secondary_email.data:
                contact.secondary_email = form.secondary_email.data

            db.session.add(contact)
            db.session.commit()

            return redirect(url_for('.client', id=contact.company_id))

        return render_template('form.html', form=form)


@main.route('/edit/magazine/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_magazine(id):
    mag = Magazine.query.get(id)

    if mag is not None:
        form = EditMag(obj=mag)

        if form.validate_on_submit():
            mag.name = form.name.data
            mag.owner = form.owner.data
            mag.sales_person = form.sales_person.data
            mag.page_count = form.page_count.data
            mag.note = form.note.data
            mag.client_mag = '{} - {}'.format(mag.owner.name, mag.name)

            if form.published.data == 'published':
                mag.published = datetime.utcnow()

                for task in mag.tasks:
                    task.active = False
                    db.session.add(task)
                    db.session.commit()

            if mag.page_count != form.page_count.data:
                for page in mag.pages:
                    db.session.delete(page)
                    db.session.commit()

                id = mag.id

                count = 1

                while count < form.page_count.data + 1:
                    page = Page(number=count, magazine_id=id)
                    db.session.add(page)
                    db.session.commit()
                    count += 1


            db.session.add(mag)
            db.session.commit()
            flash('Magazine successfully edited.')
            return redirect(url_for('.magazine', id=id))

        return render_template('form.html', form=form)

    flash('That magazine does not exist.')
    return redirect(url_for('.all_magazines'))


@main.route('/edit/task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get(id)

    if task is not None:
        mag = Magazine.query.get(task.magazine_id)
        form = EditTask(obj=task)
        form.pages.query = mag.pages

        if form.validate_on_submit():

            task.name = form.name.data
            task.description = form.description.data
            task.status = form.status.data
            task.users = form.users.data
            task.pages = form.pages.data

            if form.due_date.data:
                task.due_date = form.due_date.data

            db.session.add(task)
            db.session.commit()

            if form.comment.data:
                user = User.query.get(current_user.get_id())

                comment = Comment(posted_date=datetime.utcnow(),
                                  text=form.comment.data,
                                  poster=user,
                                  task=task)

                db.session.add(comment)
                db.session.commit()

            #Check if I could remove this line and just let the for loop run and check all the tasks
            if task.status == 'road-blocked':
                assigner = User.query.get(task.assigner.id)

                send_email(assigner.email, "One of your tasks is road blocked.",
                           "{} - {}".format(task.name, task.description), task.employee.email)

            elif task.status == 'inactive' or task.status == 'finished':
                task.active = False
                db.session.add(task)
                db.session.commit()

            else:
                task.active = True
                db.session.add(task)
                db.session.commit()

                for user in task.users:
                    send_email(user.email, "One of your tasks has been edited.",
                            """{}
                            Task: {}
                            Description: {}
                            Due Date: {}
                            Assigned by: {}""".format(mag.client_mag, task.name, task.description, task.due_date, task.assigned_by), 
                            task.assigner.email)

            for task in mag.tasks:
                if task.status == 'road-blocked':
                    mag.status = 'road-blocked'
                    db.session.commit()
                    break
            else:
                mag.status = 'active'
                db.session.commit()

            flash('Task successfully edited.')
            return redirect(url_for('.magazine', id=task.magazine_id))

        return render_template('form.html', form=form)

    return redirect(url_for('.all_magazines'))


@main.route('/archive/user/<int:id>')
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


@main.route('/archive/client/<int:id>')
@login_required
def archive_client(id):
    client = Client.query.get(id)

    if client:

        magazines = Magazine.query.filter_by(owner=client)

        if magazines:
            for magazine in magazines:
                magazine.active = False
                db.session.commit()

                for task in magazine.tasks:
                    task.active = False
                    db.session.commit()

        client.active = False
        db.session.commit()
        flash('The client, any associated magazines and their tasks have been archived.')
        return redirect(url_for('.all_clients'))

    flash('No such client exists.')
    return redirect(url_for('.all_clients'))


@main.route('/archive/magazine/<int:id>')
@login_required
def archive_magazine(id):
    magazine = Magazine.query.get(id)

    if magazine:
        for task in magazine.tasks:
                    task.active = False
                    db.session.commit()

        flash("The magazine and its tasks have been archived.")
        return redirect(url_for('.all_magazines'))

    flash('No such magazine exists.')
    return redirect(url_for('.all_magazines'))


@main.route('/delete/user/<int:id>')
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


@main.route('/delete/client/<int:id>')
@login_required
def delete_client(id):
    client = Client.query.get(id)

    if client:
        magazines = Magazine.query.filter_by(owner=client).all()

        if magazines:
            for magazine in magazines:
                for task in magazine.tasks:
                    db.session.delete(task)
                    db.session.commit()

                db.session.delete(magazine)
                db.session.commit()

        db.session.delete(client)
        db.session.commit()
        flash('The client, associated magazines and tasks have been deleted.')
        return redirect(url_for('.all_clients'))

    flash('No such client exists.')
    return redirect(url_for('.all_clients'))


@main.route('/delete/magazine/<int:id>')
@login_required
def delete_magazine(id):
    magazine = Magazine.query.get(id)

    if magazine:
        for task in magazine.tasks:
            db.session.delete(task)
            db.session.commit()

        db.session.delete(magazine)
        db.session.commit()
        flash('The magazine and associated tasks have been deleted.')
        return redirect(url_for('.all_magazines'))

    flash('No such magazine exists.')
    return redirect(url_for('.all_magazines'))


@main.route('/delete/task/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get(id)

    if task:
        db.session.delete(task)
        db.session.commit()
        flash('The task has been deleted.')
        redirect(url_for('.all_tasks'))

    flash('No such task exists.')
    return redirect(url_for('.all_tasks'))


@main.route('/users')
@login_required
def all_users():
    users = User.query.all()

    return render_template('all_users.html', users=users)


@main.route('/clients')
@login_required
def all_clients():
    clients = Client.query.filter_by(active=True).order_by(Client.name.asc()).all()

    return render_template('all_clients.html', clients=clients)


@main.route('/')
@main.route('/magazines')
@login_required
def all_magazines():
    magazines = Magazine.query.filter_by(active=True).order_by(Magazine.client_mag.asc()).all()

    return render_template('all_mags.html', magazines=magazines)


@main.route('/tasks')
@login_required
def all_tasks():
    tasks = Task.query.filter_by(active=True).order_by(Task.magazine_id.desc()).all()

    return render_template('all_tasks.html', tasks=tasks)


@main.route('/user/<int:id>')
@login_required
def user(id):
    user = User.query.get(id)

    if not user:
        flash('That user does not exist.')
        return redirect(url_for('.all_users'))

    return render_template('user.html', user=user)


@main.route('/client/<int:id>')
@login_required
def client(id):
    client = Client.query.get(id)

    if not client:
        flash('That client does not exist.')
        return redirect(url_for('.all_clients'))

    return render_template('client.html', client=client)


@main.route('/magazine/<int:id>')
@login_required
def magazine(id):
    mag = Magazine.query.get(id)

    if not mag:
        flash('That magazine does not exist')
        return redirect(url_for('.all_magazines'))

    return render_template('magazine.html', mag=mag)


@main.route('/task/<int:id>')
@login_required
def task(id):
    task = Task.query.get(id)

    if not task:
        flash('That task does not exist.')
        return redirect(url_for('.all_tasks'))

    return render_template('task.html', task=task)


@main.route('/my_tasks')
@login_required
def my_tasks():
    user = User.query.get(current_user.get_id())

    return render_template('my_tasks.html', user=user)


@main.route('/my_assignments')
@login_required
def my_assignments():
    user = User.query.get(current_user.get_id())

    return render_template('my_tasks.html', user=user)


@main.route('/call_log', methods=['GET', 'POST'])
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


@main.route('/test')
@login_required
def test():
    test = current_user.get_id()

    return render_template('test.html', test=test)