# CDManager

A basic project management system for a company specializing in custom design magazines. Currently under development.

# License

This project is free to use for any purposes under the Apache license. Attribution is required and I cannot be held liable for any issues arising from your use or modification of this software.

# Utilizes
* Flask
* Jinja2
* Flask-SQLAlchemy
* Flask-Script
* Flask-Migrate
* Flask-Login
* Flask-WTF
* Flask-Bootstrap
* Flask-Moment

# Features

* Easily see data about all of your clients (company, location, contact info, phone, magazines, and notes)
* Quickly know the status of all your active magazines
* View all the uncompleted tasks for each client/magazine on either the clients page, or their magazine page
* See all of your users active work and whether they're road blocked by anything
* Make quick and easy edits to all of the above with simple forms

Note: Screenshots coming soon. Any web designers who would like to contribute to prettifying the system are greatly appreciated as well.

# Road Map

* Add the ability to populate the database from a CSV file (Mostly done but not ready yet)
* Add automatic email to the magazines sales person when an employee is road blocked on a task
* Add automatic email to employee when they are assigned a new task
* Add option to assign tasks to specific pages of each magazine
* Expand user system to utilize roles for ease of future expansion
* Add default username/password to DB


# Getting Started

The site currently uses Flask-SQLAlchemy for database management, by default it will create a SQLite database in the application folder. There is no default username inserted into the database so you'll have to create one before you can log in and start creating clients, magazines, tasks and other users. This can be accomplished by running this in flask-script from the terminal:

    $ python run.py shell
    >>> from app import db
    >>> from app.models import User
    >>> user = User(email='youremail@addresshere.com', first_name='First', last_name='Last', password='Your Password here')
    >>> db.session.add(user)
    >>> db.session.commit()

**Note: This does not store your password in plaintext. The application will automatically encrypt using _Werkzeug.Security_**

