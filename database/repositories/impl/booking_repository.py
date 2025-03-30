from datetime import datetime

from click.testing import Result
from fastapi import Depends
from sqlalchemy import select, delete, CursorResult, update
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.booking import Booking
from database.repositories.meta.booking_repository_meta import BookingRepositoryMeta
from exceptions.generic.generic_not_found_exception import GenericNotFoundException
from utils.enum.booking_statuses import BookingStatuses


class BookingRepository(BookingRepositoryMeta):
    _db: Session = None

    def __init__(self, db: Session = Depends(Database().get_db)):
        self._db = db

    def find_all(self) -> list[Booking]:
        stmt = select(Booking)
        return list(self._db.scalars(stmt))

    def find_all_for_customer(self, customer_id) -> list[Booking]:
        stmt = select(Booking).where(Booking.customer_id == customer_id)
        return list(self._db.scalars(stmt))


    def make_reservation(self, reservation_data: Booking) -> Booking:
        self._db.add(reservation_data)
        self._db.commit()
        self._db.refresh(reservation_data)
        return reservation_data

    def edit_reservation(self, reservation_data: Booking) -> Booking:
        stmt = update(Booking).where(Booking.id == reservation_data.id).values(
            start_date=reservation_data.start_date,
            end_date=reservation_data.end_date,
            boat_id=reservation_data.boat_id,
            total_price=reservation_data.total_price,
            price_difference=reservation_data.price_difference,
            requires_refund=reservation_data.requires_refund,
            notes=reservation_data.notes,
        )
        self._db.execute(stmt)
        self._db.commit()
        self._db.flush()

        stmt_get = select(Booking).where(Booking.id == reservation_data.id)
        return self._db.scalar(stmt_get)

    """
        Questo metodo mi consente di verificare se il medesimo utente ha prenotazioni
        per il periodo richiesto. Come scelta di progettazione, voglio evitare che l'utente
        possa prenotare due imbarcazioni per lo stesso periodo.
        Torniamo True se ci sono conflitti, False altrimenti.
    """
    def check_customer_existing_bookings(self, customer_id: int, start_date: datetime, end_date: datetime) -> bool:
        stmt = select(Booking).where(
            Booking.customer_id == customer_id,
            Booking.start_date < end_date,
            Booking.end_date > start_date,
            Booking.reservation_status == BookingStatuses.CONFIRMED.value
        )
        return self._db.scalar(stmt) is not None


    def delete_booking(self, booking: Booking) -> int:
        stmt = delete(Booking).where(Booking.id == booking.id)
        result: CursorResult = self._db.execute(stmt)
        self._db.commit()
        return result.rowcount

    def get_booking(self, booking_id: int) -> Booking | None:
        stmt = select(Booking).where(Booking.id == booking_id)
        return self._db.scalar(stmt)