import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


PROJECT_NAME = 'Auth Backend'

dotenv_path = Path(f"{BASE_DIR}/.env")
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = os.getenv('SECRET_KEY')


SQL_ENGINE = os.environ.get('SQL_ENGINE')
SQL_USER = os.environ.get('SQL_USER')
SQL_PASSWORD = os.environ.get('SQL_PASSWORD')
SQL_HOST = os.environ.get('SQL_HOST')
SQL_PORT = os.environ.get('SQL_PORT')
SQL_DATABASE = os.environ.get('SQL_DATABASE')

EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "src/email-templates/build"

SMTP_TLS = os.environ.get('SMTP_TLS')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
EMAILS_FROM_EMAIL = os.environ.get('EMAILS_FROM_EMAIL')

EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL
EMAIL_TEST_USER = 'arxhangel.main@gmail.com'

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7