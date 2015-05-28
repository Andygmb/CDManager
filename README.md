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

From here you should be good to go. For instructions on using the application refer to the following section.

# Using the application

## Adding a...

### Client

1. Go to the 'Clients' tab at the top of the page
2. Select 'Add Client'
3. Enter the company name
4. Enter their address
5. Enter the main contact person's name
6. Enter their email address
7. Enter their phone number
8. Enter any additional notes about the client.
9. Submit

### Magazine

*Note: To add a new _magazine_ you must first have a _client_ to assign it to.*

1. Go to the 'Magazines' tab at the top of the page
2. Select 'Add Magazine'
3. Select the client the magazine is for, leave the published status as 'Not Published' unless the magazine is already completed.
4. Enter the magazine name (e.g. 'Comfort Zone', 'Degrees')
5. Enter the name of the sales person
6. Enter the page count of the magazine
7. Enter any additional notes about the magazine
8. Submit

### Task

*Note: To add a new _task_ you must first have an _magazine_ and a _user_ of which to assign it.*

1. Go to the 'Tasks' tab at the top of the page
2. Select 'Add Task'
3. Select the magazine from the dropdown (Note: This will only show magazines which are not set as 'Published')
4. Set the status of the task
5. Enter a task name
6. Enter a description of what the task entails
7. Enter a due date (Use the format: MM/DD/YYYY)
8. Enter any additional notes about the task
9. Submit

### User

1. Go to the 'Users' tab at the top of the page
2. Select 'Add User'
3. Enter the email address of the user
4. Enter the password
5. Confirm the password
6. Enter the first name of the user
7. Enter the last name of the user
8. Submit

## What you get in each view

### All Clients

|Name         | Contact             | Address         | Phone | Note            |
|-------------|---------------------|-----------------|-------|-----------------|
|Company Name | Contact Person Name | Company Address | Phone | Additional Notes|

The company name is also linked so you can get a view of all of the information about that individual company including all of their magazines and all of their active tasks.

### Specific Client

Client Info (Link to edit client)

|Contact             | Email         | Address         | Phone | Active                              |
|--------------------|---------------|-----------------|-------|-------------------------------------|
|Contact Person Name | Contact Email | Company Address | Phone | Whether the client is active or not |

Client Notes

Any additional notes written about the client.

Magazines

|Name          | Sales Person      | Pages      | Published                         |
|--------------|-------------------|------------|-----------------------------------|
|Magazine Name | Sales Person Name | # of Pages | Whether the magazine is published |

**Note: Each magazine is also color coded. The magazine will be green if all of the active tasks are running smoothly. It will switch to red if any of the tasks have been marked as _'Road Blocked'_.**

### All Magazines

|Company      | Magazine Name | Pages      | Contact        | Notes            |
|-------------|---------------|------------|----------------|------------------|
|Company Name | Magazine Name | # of Pages | Contact Person | Additional Notes |

**Note: The _Company_ field will link directly to that _Client_'s page. The _Magazine Name_ field will link directly to that specific magazine's page. The _Contact_ field will create a clickable link that will open a new email to that person.**

**The rows are also color coded. The row will be green if all of the tasks are running smoothly. It will switch to red if any of the tasks have been marked as _'Road Blocked'_.**

### Specific Magazine

Magazine Name (Link to edit magazine)
Company Name (Linked to that company's specific page)


Magazine Info

|Contact             | Email         | Address         | Phone | Pages                               |
|--------------------|---------------|-----------------|-------|-------------------------------------|
|Contact Person Name | Contact Email | Company Address | Phone | Whether the client is active or not |

Notes
Any notes for the magazine

Tasks

|Name      | Description      | Due Date | Assigned To                  |
|----------|------------------|----------|------------------------------|
|Task Name | Task Description | Due Data | User the task is assigned to |

**Note: The _Name_ field will also link to the individual _Task_'s page. The _Assigned To_ field will also link directly to that specific _User_'s page so you can see what that _User_ currently has assigned to them.**

### All Users

User's Tasks

|User      | Magazine             | Assigned Tasks | Task Descriptions   |
|----------|----------------------|----------------|---------------------|
|User Name | Magazine task is for | Task Name      | Description of task |
|          | Magazine task is for | Task Name      | Description of task |
|Next User | Magazine task is for | Task Name      | Description of task |
|          | Magazine task is for | Task Name      | Description of task |

**Note: The system will show every _Task_ for a specific _User_ and then show the next _User_ and all of their tasks.**

**The _User_ field will link to that specific _User_'s page. The _Magazine_ field will link directly to that specific _Magazine_'s page. The _Assigned_ _Task_'s field will link directly to that specific _Task_'s page.**

**The rows are also color coded. They will be green if they are active or red if the _Task_ is "_Road Blocked_".**

### Specific User

User Name - (Link to edit user)

|Task      | Task Description | Due Date |
|----------|------------------|----------|
|Task Name | Task description | Due Date |

**Note: The _Task_ field will link directly to that specific _Task_'s page.**
