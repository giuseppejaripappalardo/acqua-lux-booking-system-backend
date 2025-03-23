from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.booking import Booking
from database.repositories.meta.booking_repository_meta import BookingRepositoryMeta


class BookingRepository(BookingRepositoryMeta):
    _db: Session = None

    def __init__(self, db: Session = Depends(Database().get_db)):
        self._db = db

    def find_all(self) -> list[Booking]:
        stmt = select(Booking)
        return list(self._db.scalars(stmt))