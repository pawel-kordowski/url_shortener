from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class Url(Base):
    __tablename__ = "url"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    full_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False, index=True, unique=True)
