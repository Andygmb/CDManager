from flask import render_template, flash, redirect, session, url_for, request
from flask.ext.login import login_user, logout_user, login_required
from app import app, db
from models import User, Magazine, Client, Task
from forms import EditUser, EditClient, EditMag, EditMag, EditTask, LogIn
from datetime import datetime


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LogIn()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(url_for('all_magazines'))
			
		flash('Either your username or password are incorrect.')
	return render_template('form.html', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('index'))	


@app.route('/add/user', methods=['GET', 'POST'])
@login_required
def add_user():
	form = EditUser()

	if form.validate_on_submit():

		user = User.query.filter_by(email=form.email.data).first()

		if user is None:
			user = User(email=form.email.data, password=form.password.data, \
				first_name=form.first_name.data, last_name=form.last_name.data, \
				name='{} {}'.format(form.first_name.data, form.last_name.data))
			db.session.add(user)
			db.session.commit()
			flash('User succesfully added.')
			return redirect(url_for('all_users'))

		else:
			flash(str(user))

	return render_template('form.html', form=form)


@app.route('/add/client', methods=['GET', 'POST'])
@login_required
def add_client():
	form = EditClient()

	if form.validate_on_submit():
		client = Client.query.filter_by(name=form.name.data).first()

		if client is None:
			client = Client(name=form.name.data, contact=form.contact.data, email=form.email.data, \
				address=form.address.data, phone=form.phone.data, note=form.note.data, active=1)
			db.session.add(client)
			db.session.commit()
			flash('Client successfully added.')
			return redirect(url_for('all_clients'))

		else:
			flash('{} already exists.'.format(str(client)))


	return render_template('form.html', form=form)


@app.route('/add/magazine', methods=['GET', 'POST'])
@login_required
def add_magazine():
	form = EditMag()

	if form.validate_on_submit():
		mag = Magazine(name=form.name.data, owner=form.owner.data, sales_person=form.sales_person.data, \
			pages=form.pages.data, client_mag=str(form.owner.data) + ' - ' + str(form.name.data), \
			active=True, note=form.note.data)
		db.session.add(mag)
		db.session.commit()
		flash('Magazine successfully added.')
		return redirect(url_for('all_magazines'))

	return render_template('form.html', form=form)


@app.route('/add/task', methods=['GET', 'POST'])
@login_required
def add_task():
	form = EditTask()

	if form.validate_on_submit():

		task = Task(name=form.name.data, description=form.description.data,\
			create_date=datetime.utcnow(), status=form.status.data, magazine=form.magazine.data, \
			note=form.note.data, employee=form.employee.data)

		db.session.add(task)
		db.session.commit()
		flash('Task successfully added.')
		return redirect(url_for('all_tasks'))

	return render_template('form.html', form=form)


@app.route('/edit/user/<int:id>', methods=['GET', 'POST'])
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
				user.password = password=form.password.data				

			db.session.commit()
			flash('User succesfully edited.')
			return redirect(url_for('user', id=id))

		return render_template('form.html', form=form)

	flash('That user does not exist.')
	return redirect(url_for('all_users'))


@app.route('/edit/client/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
	client = Client.query.get(id)

	if client is not None:
		form = EditClient(obj=client)

		if form.validate_on_submit():
			client.name = form.name.data
			client.email = form.email.data
			client.contact = form.contact.data
			client.address = form.address.data
			client.phone = form.phone.data
			client.note = form.note.data
			
			db.session.commit()
			flash('Client successfully edited.')
			return redirect(url_for('client', id=id))

		return render_template('form.html', form=form)

	flash('That client does not exist.')
	return redirect(url_for('all_clients'))


@app.route('/edit/magazine/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_magazine(id):
	mag = Magazine.query.get(id)

	if mag is not None:
		form = EditMag(obj=mag)

		if form.validate_on_submit():
			mag.name = form.name.data
			mag.owner = form.owner.data
			mag.sales_person = form.sales_person.data
			mag.pages = form.pages.data
			mag.note = form.note.data
			mag.client_mag = '{} - {}'.format(mag.owner.name, mag.name)

			if form.published.data == 'published':
				mag.published = datetime.utcnow()

			db.session.commit()
			flash('Magazine successfully edited.')
			return redirect(url_for('magazine', id=id))

		return render_template('form.html', form=form)

	flash('That magazine does not exist.')
	return redirect(url_for('all_magazines'))


@app.route('/edit/task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
	task = Task.query.get(id)

	if task is not None:
		form = EditTask(obj=task)

		if form.validate_on_submit():

			task.name = form.name.data
			task.description = form.description.data
			task.status = form.status.data
			task.due_date = form.due_date.data
			task.magazine = form.magazine.data
			task.employee = form.employee.data
			task.note = form.note.data

			tasks = Task.query.filter_by(magazine=form.magazine.data).all()

			for task in tasks:
				if task.status == 'road-blocked':
					task.magazine.status = 'road-blocked'
					break
				else:
					task.magazine.status = 'active'

			db.session.commit()

			flash('Task successfully edited.')
			return redirect(url_for('task', id=id))

		return render_template('form.html', form=form)

	flash('That magazine does not exist.')
	return redirect(url_for('all_magazines'))


@app.route('/archive/user/<int:id>')
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
		return redirect(url_for('all_users'))

	flash('No such user exists.')
	return redirect(url_for('all_users'))


@app.route('/archive/client/<int:id>')
@login_required
def archive_client(id):
	client = Client.query.get(id)

	if client:

		magazines = Magazine.query.filter_by(owner=client)

		if magazines:
			for magazine in magazines:
				tasks = Task.query.filter_by(magazine=magazine)

				if tasks:
					for task in tasks:
						db.session.delete(task)
						db.session.commit()

				magazine.active = False
				db.session.commit()

		client.active = False
		db.session.commit()
		flash('The client and any associated magazines have been archived. Any tasks have been deleted.')
		return redirect(url_for('all_clients'))

	flash('No such client exists.')
	return redirect(url_for('all_clients'))


@app.route('/archive/magazine/<int:id>')
@login_required
def archive_magazine(id):
	magazine = Magazine.query.get(id)

	if magazine:
		tasks = Task.query.filter_by(magazine=magazine)

		if tasks:
			for task in tasks:
				db.session.delete(task)
				db.session.commit()

		magazine.active = False
		db.session.commit()
		flash("The magazine have been archived. \
					The associated tasks have been deleted.")
		return redirect(url_for('all_magazines'))

	flash('No such magazine exists.')
	return redirect(url_for('all_magazines'))


@app.route('/delete/user/<int:id>')
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
		return redirect(url_for('all_users'))

	flash('No such user exists.')
	return redirect(url_for('all_users'))


@app.route('/delete/client/<int:id>')
@login_required
def delete_client(id):
	client = Client.query.get(id)

	if client:
		magazines = Magazine.query.filter_by(owner=client).all()

		if magazines:
			for magazine in magazines:
				tasks = Task.query.filter_by(magazine=magazine).all()
				
				if tasks:
					for task in tasks:
						db.session.delete(task)
						db.session.commit()

				db.session.delete(magazine)
				db.session.commit()
		
		db.session.delete(client)
		db.session.commit()
		flash('The client, associated magazines and tasks have been deleted.')
		return redirect(url_for('all_clients'))

	flash('No such client exists.')
	return redirect(url_for('all_clients'))


@app.route('/delete/magazine/<int:id>')
@login_required
def delete_magazine(id):
	magazine = Magazine.query.get(id)

	if magazine:
		tasks = Task.query.filter_by(magazine=magazine).all()
				
		if tasks:
			for task in tasks:
				db.session.delete(task)
				db.session.commit()

		db.session.delete(magazine)
		db.session.commit()
		flash('The magazine and associated tasks have been deleted.')
		return redirect(url_for('all_magazines'))

	flash('No such magazine exists.')
	return redirect(url_for('all_magazines'))


@app.route('/delete/task/<int:id>')
@login_required
def delete_task(id):
	task = Task.query.get(id)

	if task:
		db.session.delete(task)
		db.session.commit()

	flash('No such task exists.')
	return redirect(url_for('all_tasks'))


@app.route('/users')
@login_required
def all_users():
	users = User.query.all()

	return render_template('all_users.html', users=users)


@app.route('/clients')
@login_required
def all_clients():

	clients = Client.query.filter_by(active=True).order_by('name asc').all()

	return render_template('all_clients.html', clients=clients)


@app.route('/')
@app.route('/magazines')
@login_required
def all_magazines():
	magazines = Magazine.query.filter_by(active=True).order_by('client_mag asc').all()		

	return render_template('all_mags.html', magazines=magazines)


@app.route('/tasks')
@login_required
def all_tasks():
	tasks = Task.query.all()

	return render_template('all_tasks.html', tasks=tasks)


@app.route('/user/<int:id>')
@login_required
def user(id):
	user = User.query.get(id)

	if not user:
		flash('That user does not exist.')
		return redirect(url_for('all_users'))

	return render_template('user.html', user=user)


@app.route('/client/<int:id>')
@login_required
def client(id):
	client = Client.query.get(id)

	if not client:
		flash('That client does not exist.')
		return redirect(url_for('all_clients'))

	return render_template('client.html', client=client)


@app.route('/magazine/<int:id>')
@login_required
def magazine(id):
	mag = Magazine.query.get(id)

	if not mag:
		flash('That magazine does not exist')
		return redirect(url_for('all_magazines'))

	return render_template('magazine.html', mag=mag)


@app.route('/task/<int:id>')
@login_required
def task(id):
	task = Task.query.get(id)

	if not task:
		flash('That task does not exist.')
		return redirect(url_for('all_tasks'))

	return render_template('task.html', task=task)


@app.route('/test')
@login_required
def test():
	client = Client.query.filter_by(name='Estes Air').first()

	test = Magazine.query.filter_by(owner=client).order_by('id desc').first()

	return render_template('test.html', test=test)