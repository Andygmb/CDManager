from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_required
from .. import db
from ..models import Magazine, Page, Task
from . import magazines
from .forms import EditMag
from datetime import datetime


@magazines.route('/')
@login_required
def all_magazines():
    magazines = Magazine.query.filter_by(active=True).order_by(Magazine.client_mag.asc()).all()

    return render_template('all_mags.html', magazines=magazines)


@magazines.route('/<int:id>')
@login_required
def magazine(id):
    mag = Magazine.query.get(id)

    if not mag:
        flash('That magazine does not exist')
        return redirect(url_for('.all_magazines'))

    return render_template('magazine.html', mag=mag)


@magazines.route('/add', methods=['GET', 'POST'])
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


@magazines.route('/edit/<int:id>', methods=['GET', 'POST'])
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
                mag.active = False
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


@magazines.route('/archive/<int:id>')
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


@magazines.route('/delete/magazine/<int:id>')
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


