from datetime import datetime, timedelta, timezone

from exceptions.dates.InvalidDatetimeException import InvalidDatetimeException
from exceptions.generic.integrity_database_exception import IntegrityDatabaseException
from models.request.booking.search_boat_request import SearchBoatRequest
from utils.datetime_provider import DateTimeProvider
from utils.enum.messages import Messages
from utils.logger_service import LoggerService


def booking_validator(booking_request: SearchBoatRequest):
    current_date = datetime.now(timezone.utc)
    logger_service = LoggerService().logger

    """
        Di default il frontend è configurato per mandare date in formato UTC e mostrarle all'utente in formato Europe/Rome.
        Per sicurezza in ogni caso chiamiamo parse_input_datetime_to_utc per controllare se è presente il timezone ed è corretto.
        Il metodo restituisce un datetime valido in formato UTC.
    """
    booking_request.start_date = DateTimeProvider.parse_input_datetime_to_utc(booking_request.start_date)
    booking_request.end_date = DateTimeProvider.parse_input_datetime_to_utc(booking_request.end_date)

    logger_service.info(f"start date: {booking_request.start_date}")
    logger_service.info(f"end date: {booking_request.end_date}")

    """
        A questo punto inizamo a fare le validazioni delle date.
        Se la data di inizio è maggiore di quella di fine, lancio un ValueError.
    """
    if booking_request.start_date >= booking_request.end_date:
        raise InvalidDatetimeException(message=Messages.START_DATE_GREATHER_OR_EQUAL_THAN.value)


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

    """
        Qui controlliamo la durata minima della prenotazione.
        Se l'intervallo tra la data di fine e la data di inizio è inferiore a 1 ora,
        lanciamo un InvalidDatetimeException.
    """
    if booking_request.end_date - booking_request.start_date < timedelta(hours=1):
        raise InvalidDatetimeException(message=Messages.MIN_DURATION_NOT_SATISFIED.value)

    """
        Ci assicuriamo che il numero di posti richiesto sia almeno 1.
    """
    if booking_request.seat < 1:
        raise IntegrityDatabaseException(Messages.MINIMUM_SEAT_REQUEST.value)
