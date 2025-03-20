from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Relationship

from database.entities import Base
from utils.datetime_provider import DateTimeProvider

class Role(Base):

    __tablename__ = 'roles'
    role = Relationship("Users", back_populates="roles")
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)
    modified_at = Column(DateTime, server_default=DateTimeProvider.get_timestamp_utc_sql(), onupdate=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)