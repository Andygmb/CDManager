from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required
from .. import db
from ..models import Client, Contact, Magazine
from . import clients
from .forms import EditClient, EditContact


@clients.route('/')
@login_required
def all_clients():
    clients = Client.query.filter_by(active=True).order_by(Client.name.asc()).all()

    return render_template('all_clients.html', clients=clients)


@clients.route('/<int:id>')
@login_required
def client(id):
    client = Client.query.get(id)

    if not client:
        flash('That client does not exist.')
        return redirect(url_for('.all_clients'))

    return render_template('client.html', client=client)


@clients.route('/add', methods=['GET', 'POST'])
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
            return redirect(url_for('.client', id=client.id))

        else:
            flash('{} already exists.'.format(str(client)))

    return render_template('form.html', form=form)


@clients.route('/edit/<int:id>', methods=['GET', 'POST'])
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


@clients.route('/archive/client/<int:id>')
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


@clients.route('/delete/<int:id>')
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


@clients.route('/<int:client_id>/add/contact', methods=['GET', 'POST'])
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
            contact.secondary_email = form.secondary_email.data
        if form.secondary_phone.data:
            contact.secondary_phone = form.secondary_phone.data

        db.session.add(contact)
        db.session.commit()

        return redirect(url_for('.client', id=client.id))

    return render_template('form.html', form=form)


@clients.route('/edit/contact/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    contact = Contact.query.get(id)

    if contact:
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

    flash('No such contact exists.')
    return redirect(url_for('.all_clients'))


@clients.route('/delete/contact/<int:id>')
@login_required
def delete_contact(id):
    contact = Contact.query.get(id)

    if contact is not None:
        db.session.delete(contact)
        db.session.commit()

        return redirect(url_for('magazines.magazine', id=request.args.get('client')))