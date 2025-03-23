from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from database.entities.base import Base
from utils.enum.boat_statuses_values import BoatStatusesValues


class BoatStatuses(Base):
    """
        In questo model definiamo i campi, i relativi datatype ed eventuali constraint
    """
    __tablename__ = 'boat_statuses'
    id: Mapped[int] = mapped_column(Integer,primary_key=True, index=True, autoincrement=True, nullable=False)
    name: Mapped[BoatStatusesValues] = mapped_column(Enum(BoatStatusesValues, create_constraint=True), index=True, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), index=True, nullable=False)