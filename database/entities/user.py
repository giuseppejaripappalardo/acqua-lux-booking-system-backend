from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.entities.base import Base
from database.entities.role import Role
from utils.datetime_provider import DateTimeProvider


class User(Base):
    """
        In questo model definiamo i campi, i relativi datatype ed eventuali constraint
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    lastname: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    modified_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    role: Mapped["Role"] = relationship("Role", lazy="joined")
