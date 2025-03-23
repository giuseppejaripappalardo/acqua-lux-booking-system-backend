from fastapi import Depends
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.boat import Boat
from database.entities.booking import Booking
from database.repositories.meta.boat_repository_meta import BoatRepositoryMeta
from models.request.booking.booking_request import BookingRequest


class BoatRepository(BoatRepositoryMeta):
    _db: Session = None

    def __init__(self, db: Session = Depends(Database().get_db)):
        self._db = db

    def find_all(self) -> list[Boat]:
        stmt = select(Boat)
        return list(self._db.scalars(stmt))

    def find_available_boats_for_booking(self, booking_request: BookingRequest) -> list[Boat]:
        stmt = (
            select(Boat)
            .outerjoin(Boat.bookings)
            .where(
                or_(
                    Booking.id.is_(None),
                    or_(
                        Booking.end_date <= booking_request.start_date,
                        Booking.start_date >= booking_request.end_date
                    )
                )
            )
        )
        return list(self._db.scalars(stmt))
