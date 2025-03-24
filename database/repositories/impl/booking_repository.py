from click.testing import Result
from fastapi import Depends
from sqlalchemy import select, delete, CursorResult
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.booking import Booking
from database.repositories.meta.booking_repository_meta import BookingRepositoryMeta
from exceptions.generic.generic_not_found_exception import GenericNotFoundException


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

    def delete_booking(self, booking: Booking) -> int:
        stmt = delete(Booking).where(Booking.id == booking.id)
        result: CursorResult = self._db.execute(stmt)
        self._db.commit()
        deleted_count =  result.rowcount
        return deleted_count

    def get_booking(self, booking_id: int) -> Booking | None:
        stmt = select(Booking).where(Booking.id == booking_id)
        return self._db.scalar(stmt)