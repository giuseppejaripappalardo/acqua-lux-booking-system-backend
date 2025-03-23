from fastapi import Depends
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.boat import Boat
from database.entities.boat_statuses import BoatStatuses
from database.entities.booking import Booking
from database.repositories.meta.boat_repository_meta import BoatRepositoryMeta
from models.request.booking.search_boat_request import SearchBoatRequest
from utils.enum.boat_statuses_values import BoatStatusesValues
from utils.logger_service import LoggerService


class BoatRepository(BoatRepositoryMeta):
    _db: Session = None
    _logger_service: LoggerService = None

    def __init__(self, db: Session = Depends(Database().get_db),
                 logger_service: LoggerService = Depends(LoggerService)):
        self._db = db
        self._logger_service = logger_service

    def find_all(self) -> list[Boat]:
        stmt = select(Boat)
        return list(self._db.scalars(stmt))

    def find_available_boats_for_booking(self, booking_request: SearchBoatRequest) -> list[Boat]:
        stmt = (
            select(Boat)
            .join(BoatStatuses)
            .outerjoin(
                Booking,
                and_(
                    Booking.boat_id == Boat.id,
                    Booking.start_date < booking_request.end_date,
                    Booking.end_date > booking_request.start_date
                )
            )
            .where(
                BoatStatuses.name == BoatStatusesValues.AVAILABLE.value,
                Boat.seat >= booking_request.seat,
                Booking.id.is_(None)  # Nessun booking in conflitto
            )
        )
        return list(self._db.scalars(stmt))

    def get_boat_to_book(self, booking_request: SearchBoatRequest) -> Boat:
        stmt_boat = (
            select(Boat)
            .join(BoatStatuses)
            .outerjoin(
                Booking,
                and_(
                    Booking.boat_id == Boat.id,
                    Booking.start_date < booking_request.end_date,
                    Booking.end_date > booking_request.start_date
                )
            )
            .where(
                BoatStatuses.name == BoatStatusesValues.AVAILABLE.value,
                Boat.seat >= booking_request.seat,
                Boat.id == booking_request.boat_id,
                Booking.id.is_(None)
            )
        )
        return self._db.scalar(stmt_boat)