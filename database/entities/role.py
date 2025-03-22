from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.entities.base import Base
from utils.datetime_provider import DateTimeProvider


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)
    modified_at: Mapped[datetime] =  mapped_column(DateTime, server_default=DateTimeProvider.get_timestamp_utc_sql(), onupdate=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)
