import logging
from celery.task import task

from .functions import send_user_notification


log = logging.getLogger(__name__)


@task(name='send-email-task')
def send_email_task(subject, notification, from_email, to_email):
    """
    Task for send email to user. And log result of operation.
    :param subject: Email subject
    :param notification: Email text
    :param from_email: sender email
    :param to_email: receiver email
    :return: None
    """
    try:
        send_user_notification(subject, notification, from_email, to_email)
        log_string = "Email was sent to {email}. Subject {subject}".format(email=to_email, subject=subject)
        log.debug(log_string)
    except Exception:
        log_string = "Failed to send email to {email}. Subject {subject}".format(email=to_email, subject=subject)
        log.error(log_string)