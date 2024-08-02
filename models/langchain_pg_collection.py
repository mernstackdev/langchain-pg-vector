import uuid
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID

from utils.database import Base

class Collection(Base):
    __tablename__ = 'langchain_pg_collection'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    cmetadata = Column(JSON, nullable=True)