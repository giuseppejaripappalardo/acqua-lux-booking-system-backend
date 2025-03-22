from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.entities.base import Base


class BoatsStatuses(Base):
    """
        In questo model definiamo i campi, i relativi datatype ed eventuali constraint
    """
    __tablename__ = 'boats_statuses'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), index=True, nullable=False)