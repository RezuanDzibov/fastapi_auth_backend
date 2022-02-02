from datetime import datetime

from sqlalchemy import Column, String, DATE, DateTime, Boolean

from src.base.models import UUIDMixin
from src.core import Base


class User(UUIDMixin, Base):
    __tablename__ = 'users'

    username = Column(String(length=255), unique=True)
    email = Column(String(length=255), unique=True)
    password = Column(String(length=100))
    first_name = Column(String(length=100))
    last_name = Column(String(length=100))
    birth_date = Column(DATE)
    join_date_time = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)