from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from src.base.models import UUIDMixin
from src.core.db import Base
from src.user.models import User


class Verification(UUIDMixin, Base):
    __tablename__ = 'verification_codes'

    user_id = Column(UUID, ForeignKey(User.id))
    user = relationship('User', backref=backref('verification_code', uselist=False))