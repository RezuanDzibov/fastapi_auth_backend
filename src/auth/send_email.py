from config import settings
from src.base.utils.email import send_email


def send_new_account_email(email_to: str, username: str, password: str, uuid: str):
    verification_link = f'http://{settings.SERVER_HOST}/auth/confirm-email/{uuid}'
    subject = 'A new user'
    send_email(
        email_to=email_to,
        template_name='new_account.html',
        subject=subject,
        environment={
            'project_name': settings.PROJECT_NAME,
            'username': username,
            'password': password,
            'email': email_to,
            'link': verification_link,
        },
    )
    
    
def send_reset_password_email(email_to: str, email: str, token: str):
    if hasattr(token, 'decode'):
        use_token = token.decode() # type: ignore
    else:
        use_token = token
    recovery_link = f'http://{settings.SERVER_HOST}/reset-password?token={use_token}'
    subject = f'Password recovery for user {email}'
    send_email(
        email_to=email_to,
        template_name='reset_password.html',
        subject=subject,
        environment={
            'project_name': settings.PROJECT_NAME,
            'username': email,
            'email': email_to,
            'valid_minutes': settings.EMAIL_RESET_TOKEN_EXPIRE,
            'link': recovery_link,
        }
    )