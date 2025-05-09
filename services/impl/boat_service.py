from fastapi import Depends

from database.entities.boat import Boat
from database.repositories.impl.boat_repository import BoatRepository
from database.repositories.meta.boat_repository_meta import BoatRepositoryMeta
from models.request.booking.search_boat_request import SearchBoatRequest, EditSearchBoatRequest
from services.meta.boat_service_meta import BoatServiceMeta
from utils.datetime_provider import DateTimeProvider
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

    def find_available_boats_for_booking(self, booking_request: SearchBoatRequest | EditSearchBoatRequest) -> list[Boat]:
        existing_booking_id = None

        if isinstance(booking_request, EditSearchBoatRequest) and booking_request.booking_id is not None:
            existing_booking_id = booking_request.booking_id

        # Metodo preposto alla validazione
        # Consultare l'implementazione per avere tutti i dettagli.
        booking_validator(booking_request)

        """
            Solo per una questione di chiarezza faccio il controllo anche qui sul timezone.
            Considerando che comunque 
        """
        booking_request.start_date = DateTimeProvider.parse_input_datetime_to_utc(booking_request.start_date)
        booking_request.end_date = DateTimeProvider.parse_input_datetime_to_utc(booking_request.end_date)

        return self._boat_repository.find_available_boats_for_booking(booking_request, existing_booking_id)
