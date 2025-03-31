from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.entities.base import Base
from utils.datetime_provider import DateTimeProvider
from utils.enum.roles import Roles


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name: Mapped[Roles] = mapped_column( Enum(Roles, create_constraint=True), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    modified_at: Mapped[datetime] =  mapped_column(DateTime, onupdate=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)
