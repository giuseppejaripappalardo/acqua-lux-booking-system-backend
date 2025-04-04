from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, DECIMAL, ForeignKey, String, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.entities.base import Base
from utils.enum.booking_statuses import BookingStatuses
from utils.enum.payment_methods import PaymentMethods


class Booking(Base):
    """
        In questo model definiamo i campi, i relativi datatype ed eventuali constraint
    """
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    seat: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    boat_id: Mapped[int] = mapped_column(Integer, ForeignKey("boats.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    reservation_code: Mapped[str] = mapped_column(String(255), nullable=False)
    payment_method: Mapped[PaymentMethods] = mapped_column(Enum(PaymentMethods, create_constraint=True))
    reservation_status: Mapped[BookingStatuses] = mapped_column(Enum(BookingStatuses, create_constraint=True), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    modified_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    price_difference: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=Decimal(0), nullable=True)
    requires_refund: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    boat: Mapped["Boat"] = relationship("Boat", back_populates="bookings", lazy="joined")
    customer: Mapped["User"] = relationship("User", lazy="joined")