from datetime import datetime, timedelta

import pytz
from fastapi import Depends

from database.entities.boat import Boat
from database.repositories.impl.boat_repository import BoatRepository
from database.repositories.meta.boat_repository_meta import BoatRepositoryMeta
from exceptions.dates.InvalidDatetimeException import InvalidDatetimeException
from models.request.booking.booking_request import BookingRequest
from services.meta.boat_service_meta import BoatServiceMeta
from utils.logger_service import LoggerService
from utils.messages import Messages


class BoatService(BoatServiceMeta):
    _logger_service: LoggerService.logger = None
    _boat_repository: BoatRepositoryMeta = None

    def __init__(self, log_service: LoggerService = Depends(LoggerService),
                 boat_repository: BoatRepositoryMeta = Depends(BoatRepository)):
        self._logger_service = log_service.logger
        self._boat_repository = boat_repository

    def find_all(self) -> list[Boat]:
        return self._boat_repository.find_all()

    def find_available_boats_for_booking(self, booking_request: BookingRequest) -> list[Boat]:
        default_rome_timezone = pytz.timezone("Europe/Rome")

        """
            Se il timezone della start date in input non è definito
            lo settiamo noi a Europe/Rome come definito di default per questo project work.
        """
        if booking_request.start_date.tzinfo is None:
            booking_request.start_date = default_rome_timezone.localize(booking_request.start_date)

        """
            Se il timezone della end date in input non è definito
            lo settiamo noi a Europe/Rome come definito di default per questo project work.
        """
        if booking_request.end_date.tzinfo is None:
            booking_request.end_date = default_rome_timezone.localize(booking_request.end_date)

        """
            In questo stage siamo sicuri di avere un timezone coerente per start date ed end date.
            Quindi possiamo convertire tutte le date in UTC in maniera confidente, cosi da garantire
            uniformità. Considerato che tutte le date salvate a DB sono in formato UTC.
        """
        booking_request.start_date = booking_request.start_date.astimezone(pytz.utc)
        booking_request.end_date = booking_request.end_date.astimezone(pytz.utc)

        """
            A questo punto inizamo a fare le validazioni delle date.
            Se la data di inizio è maggiore di quella di fine, lancio un ValueError.
        """
        if booking_request.start_date >= booking_request.end_date:
           raise InvalidDatetimeException(message=Messages.START_DATE_GREATHER_OR_EQUAL_THAN.value)

        current_date = datetime.now(pytz.utc)
        if booking_request.start_date < current_date:
            raise InvalidDatetimeException(message=Messages.START_DATE_LESS_THAN_CURRENT.value)

        """
            Aggiungiamo giusto un controllo mettendo un buffer di 1 ora.
            Non posso prenotare una imbarcazione subito, ma dall'ora di prenotazione devo almeno
            dare un tempo di 1 ora per far partire la prenotazione.
        """
        current_date_with_buffer = current_date + timedelta(hours=1)
        if booking_request.start_date < current_date_with_buffer:
            raise InvalidDatetimeException(message=Messages.START_DATE_NEEDS_BUFFER.value)


        # TODO GESTIRE CASO IN CUI IL MEDESIMO UTENTE PROVA A PRENOTARE UNA IMBARCAZIONE IN UN RANGE TEMPORALE CHE OVERLAPPA


        return self._boat_repository.find_available_boats_for_booking(booking_request)
