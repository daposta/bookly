from celery import Celery

from src import mail
from src.mail import create_message

celery_app = Celery()
celery_app.config_from_object("src.config")


@celery_app.task()
def send_email(email, subject, html):
    message = create_message(
        recipients=[email], subject="Verify your account", body=html
    )

    # bg_tasks.add_task(mail.send_message, message)
    mail.send_message.delay(message)
