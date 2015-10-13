from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_required, current_user
from .. import db
from ..utilities import sg, send_email
from ..models import User, Magazine, Task, Comment
from . import tasks
from .forms import EditTask, EditComment
from datetime import datetime


@tasks.route('/')
@login_required
def all_tasks():
    tasks = Task.query.filter_by(active=True).order_by(Task.magazine_id.desc()).all()

    return render_template('all_tasks.html', tasks=tasks)


@tasks.route('/<int:id>')
@login_required
def task(id):
    task = Task.query.get(id)

    if not task:
        flash('That task does not exist.')
        return redirect(url_for('.all_tasks'))

    return render_template('task.html', task=task)


@tasks.route('/my_tasks')
@login_required
def my_tasks():
    user = User.query.get(current_user.get_id())

    return render_template('my_tasks.html', user=user)


@tasks.route('/my_assignments')
@login_required
def my_assignments():
    user = User.query.get(current_user.get_id())

    return render_template('my_tasks.html', user=user)


@tasks.route('/<int:mag>/add', methods=['GET', 'POST'])
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

                for user in task.users:
                    send_email(user.email, "One of your tasks has been road-blocked.",
                            """{}
                            Task: {}
                            Description: {}
                            Due Date: {}
                            Assigned by: {}""".format(mag.client_mag, task.name, task.description, task.due_date, task.assigned_by),
                            task.assigner.email)

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
            return redirect(url_for('magazines.magazine', id=mag.id))

        return render_template('form.html', form=form)

    flash('That magazine does not exist.')
    return render_template(url_for('magazines.all_magazines'))


@tasks.route('/edit/<int:id>', methods=['GET', 'POST'])
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

                for user in task.users:
                    send_email(user.email, "One of your tasks has been road-blocked.",
                            """{}
                            Task: {}
                            Description: {}
                            Due Date: {}
                            Assigned by: {}""".format(mag.client_mag, task.name, task.description, task.due_date, task.assigned_by),
                            task.assigner.email)

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
            return redirect(url_for('magazines.magazine', id=task.magazine_id))

        return render_template('form.html', form=form)

    return redirect(url_for('magazines.all_magazines'))


@tasks.route('/delete/<int:id>')
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


@tasks.route('edit/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):

    comment = Comment.query.get(id)

    if current_user.role_id != 1:
        flash("Your permissions do not enable you to edit comments.")
        return redirect(url_for('tasks.task', id=comment.id))

    if comment is not None:
        form = EditComment(obj=comment)

        if form.validate_on_submit():
            comment.poster = form.poster.data
            comment.body = form.text.data
            comment.posted_date = form.posted_date.data

            db.session.add(comment)
            db.session.commit()

            flash('Task successfully edited.')
            return redirect(url_for('tasks.task', id=comment.task_id))

        return render_template('form.html', form=form)

    flash("No such comment exists")
    return redirect(url_for('tasks.all_tasks'))


@tasks.route('delete/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):

    comment = Comment.query.get(id)

    if current_user.role_id != 1:
        flash("Your permissions do not enable you to delete comments.")
        return redirect(url_for('tasks.task', id=comment.id))

    id = comment.task_id

    db.session.delete(comment)
    db.session.commit()

    flash("Comment successfully deleted.")
    return redirect(url_for('tasks.task', id=id))
