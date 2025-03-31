from fastapi import Depends

from database.entities.boat import Boat
from database.repositories.impl.boat_repository import BoatRepository
from database.repositories.meta.boat_repository_meta import BoatRepositoryMeta
from models.request.booking.search_boat_request import SearchBoatRequest
from services.meta.boat_service_meta import BoatServiceMeta
from utils.logger_service import LoggerService
from utils.validation.booking_validator import booking_validator


class BoatService(BoatServiceMeta):
    _logger_service: LoggerService.logger = None
    _boat_repository: BoatRepositoryMeta = None

    def __init__(self, log_service: LoggerService = Depends(LoggerService),
                 boat_repository: BoatRepositoryMeta = Depends(BoatRepository)):
        self._logger_service = log_service.logger
        self._boat_repository = boat_repository

    def find_all(self) -> list[Boat]:
        return self._boat_repository.find_all()

    def find_available_boats_for_booking(self, booking_request: SearchBoatRequest) -> list[Boat]:
        # Metodo preposto alla validazione
        # Consultare l'implementazione per avere tutti i dettagli.
        booking_validator(booking_request)
        return self._boat_repository.find_available_boats_for_booking(booking_request)
