from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.entities.base import Base
from utils.datetime_provider import DateTimeProvider


class Boat(Base):
    """
        In questo model definiamo i campi, i relativi datatype ed eventuali constraint
    """
    __tablename__ = 'boats'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    seat: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_hour: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    boat_status_id: Mapped[bool] = mapped_column(ForeignKey("boats_statuses.id"), nullable=False, index=True)
    boats_statuses: Mapped["BoatsStatuses"] = relationship("BoatsStatuses", lazy="joined")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)
    modified_at: Mapped[datetime] = mapped_column(DateTime, server_default=DateTimeProvider.get_timestamp_utc_sql(), onupdate=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)
