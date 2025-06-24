from celery import Celery
from pydantic import EmailStr
from asgiref.sync import async_to_sync
from src import mail
from src.mail import create_message

celery_app = Celery()
celery_app.config_from_object("src.config")


@celery_app.task()
def send_email(recipients: list[EmailStr], subject: str, body: str):
    message = create_message(
        recipients=recipients, subject="Verify your account", body=body
    )

    async_to_sync(mail.send_message)(message)
