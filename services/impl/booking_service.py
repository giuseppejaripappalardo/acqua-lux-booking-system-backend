from fastapi import Depends

from database.entities.booking import Booking
from database.repositories.impl.booking_repository import BookingRepository
from database.repositories.meta.booking_repository_meta import BookingRepositoryMeta
from services.meta.booking_service_meta import BookingServiceMeta
from utils.logger_service import LoggerService


class BookingService(BookingServiceMeta):
    _logger_service: LoggerService.logger = None
    _booking_repository: BookingRepositoryMeta = None

    def __init__(self, log_service: LoggerService = Depends(LoggerService),
                 booking_repository: BookingRepositoryMeta = Depends(BookingRepository)):
        self._logger_service = log_service
        self._booking_repository = booking_repository

    def find_all(self) -> list[Booking]:
        return self._booking_repository.find_all()
