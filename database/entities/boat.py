from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, DateTime, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.util import hybridproperty

from database.entities.base import Base
from database.entities.boat_statuses import BoatStatuses
from utils.datetime_provider import DateTimeProvider


class Boat(Base):
    """
        In questo model definiamo i campi, i relativi datatype ed eventuali constraint
    """
    __tablename__ = 'boats'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    seat: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_hour: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    location: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    boat_status_id: Mapped[int] = mapped_column(Integer, ForeignKey("boat_statuses.id"), nullable=False, index=True)
    boat_status: Mapped["BoatStatuses"] = relationship("BoatStatuses", lazy="joined")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="boat", lazy="select")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)
    modified_at: Mapped[datetime] = mapped_column(DateTime, server_default=DateTimeProvider.get_timestamp_utc_sql(), onupdate=DateTimeProvider.get_timestamp_utc_sql(), nullable=False)

    @hybridproperty
    def is_available(self):
        return "Yes"