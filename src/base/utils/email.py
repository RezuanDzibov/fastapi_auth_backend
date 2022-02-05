from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from jinja2 import Environment, FileSystemLoader

from config import settings


password_reset_jwt_subject = 'preset'


def send_email(email_to: str, subject: str, template_name: str, environment: dict):
    env = Environment(loader=FileSystemLoader(settings.EMAIL_TEMPLATES_DIR))
    template = env.get_template(template_name)
    output = template.render(environment)
    from_email = settings.SMTP_USER
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = email_to
    message.attach(MIMEText(output, 'html'))
    message_body = message.as_string()
    with SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp_server: # type: ignore
        smtp_server.starttls() # type: ignore
        smtp_server.login(settings.SMTP_USER, settings.SMTP_PASSWORD) # type: ignore
        smtp_server.sendmail(from_email, email_to, message_body) # type: ignore