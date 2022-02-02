from config import settings
from src.base.utils.email import send_email


def send_new_account_email(email_to: str, username: str, password: str, uuid: str):
    verification_link = f'http://{settings.SERVER_HOST}/auth/confirm-email/{uuid}'
    send_email(
        email_to=email_to,
        template_name='new_account.html',
        environment={
            'project_name': settings.PROJECT_NAME,
            'username': username,
            'password': password,
            'email': email_to,
            'link': verification_link,
        },
    )