from .app import db
from .app.models import Task
from .app.main.views import sg, send_email
from datetime import datetime

now = datetime.now()

tasks = Task.query.filter_by(status='active').all()

for task in tasks:
	if task.due_date < now:
		send_email(task.assigner.email, \
			'One of your tasks has passed its due date', "{} - {}".format(task.name, task.description), 'matt@customdm.com')