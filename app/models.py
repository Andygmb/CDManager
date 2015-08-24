from . import db
from flask.ext.login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    name = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    assignments = db.relationship('Task', backref='assigner', lazy='dynamic', foreign_keys='Task.assigned_by')
    magazines = db.relationship('Magazine', backref='sales_person', lazy='dynamic')
    comments = db.relationship('Comment', backref='poster', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.name)


class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    permissions = db.Column(db.Integer, default=2)
    users = db.relationship('User', backref='role', lazy='dynamic')


class Client(db.Model):

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    active = db.Column(db.Boolean, default=True)
    note = db.Column(db.Text)
    magazines = db.relationship('Magazine', backref='owner', lazy='dynamic')
    contacts = db.relationship('Contact', backref='company', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


class Contact(db.Model):

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    main_email = db.Column(db.String(60), unique=True)
    secondary_email = db.Column(db.String(60), unique=True)
    main_phone = db.Column(db.String(15))
    secondary_phone = db.Column(db.String(15))
    company_id = db.Column(db.Integer, db.ForeignKey('clients.id'))


class Magazine(db.Model):

    __tablename__ = 'magazines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    client_mag = db.Column(db.String(120))
    page_count = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    published = db.Column(db.DateTime)
    note = db.Column(db.Text)
    status = db.Column(db.String(40), default='active')
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    sales_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pages = db.relationship('Page', backref='magazine', lazy='dynamic')
    tasks = db.relationship('Task', backref='magazine', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


pages_tasks = db.Table('pages_tasks',
                       db.Column('page_id', db.Integer, db.ForeignKey('pages.id')),
                       db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'))
                       )


class Page(db.Model):

    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(120))
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazines.id'))
    tasks = db.relationship('Task', secondary=pages_tasks,
                            backref=db.backref('pages', lazy='dynamic'), lazy='dynamic')


tasks_users = db.Table('tasks_users',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')))


class Task(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    comments = db.relationship('Comment', backref='task', lazy='dynamic')
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazines.id'))
    users = db.relationship('User', secondary=tasks_users,
        backref=db.backref('tasks', lazy='dynamic'))
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '{}'.format(self.name)


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    posted_date = db.Column(db.DateTime)
    text = db.Column(db.Text)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))


class Call(db.Model):

    __tablename__ = 'calls'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150))
    person = db.Column(db.String(70))
    notes = db.Column(db.Text)
    called_date = db.Column(db.DateTime)