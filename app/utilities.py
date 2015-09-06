from sendgrid import SendGridClientError, SendGridServerError
import sendgrid
import os


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
        return redirect(url_for('tasks.all_tasks'))
    except SendGridServerError:
        flash('There was a problem sending the email.')
        return redirect(url_for('tasks.all_tasks'))
