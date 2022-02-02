import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)