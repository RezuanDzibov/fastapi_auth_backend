from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from src.models.base import UUIDMixin
from src.models.db import Base
from src.models.user import User


class Verification(UUIDMixin, Base):
    __tablename__ = 'verification_codes'

    user_id = Column(UUID, ForeignKey(User.id))
    user = relationship('User', backref=backref('verification_code', uselist=False))