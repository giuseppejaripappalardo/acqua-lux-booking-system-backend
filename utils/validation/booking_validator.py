from datetime import datetime, timedelta

import pytz

from exceptions.dates.InvalidDatetimeException import InvalidDatetimeException
from exceptions.generic.integrity_database_exception import IntegrityDatabaseException
from models.request.booking.search_boat_request import SearchBoatRequest
from utils.enum.messages import Messages
from utils.logger_service import LoggerService


def booking_validator(booking_request: SearchBoatRequest):
    """
        Valida i parametri per richieste di prenotazione (ricerca, inserimento, modifica).

        Questa funzione esegue le seguenti operazioni:

        - Validazione cronologica delle date:
            - La data di inizio `start_date` deve essere precedente alla data di fine `end_date`.
            - La data di inizio deve essere futura rispetto all'ora corrente, applicando un buffer minimo di 1 ora per evitare prenotazioni immediate.

        - Gestione dei timezone:
            - Se gli oggetti datetime ricevuti non specificano un timezone, viene assunto come default il timezone `Europe/Rome`.
            - Tutti i datetime con timezone, a questo punto, vengono convertiti in UTC, garantendo uniformità nella memorizzazione dei dati (tutte le date nel DB sono salvate in UTC).

        - Validazione del numero di posti richiesti:
            - Il numero di posti `seat_number` deve essere almeno 1.

        Si utilizza la classe `SearchBoatRequest` per sfruttarne il polimorfismo, consentendo così il riutilizzo della logica per classi derivate, come `BookingRequest`, evitando duplicazioni (principio DRY).

        Args:
            booking_request (SearchBoatRequest): Oggetto della richiesta con i parametri da validare.

        Raises:
            InvalidDatetimeException: Se le date non rispettano i vincoli sopraindicati.
            IntegrityDatabaseException: Se il numero di posti richiesto è inferiore a 1.
    """

    logger_service = LoggerService().logger
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

    logger_service.info(f"start date: {booking_request.start_date}")
    logger_service.info(f"end date: {booking_request.end_date}")

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

    if booking_request.seat < 1:
        raise IntegrityDatabaseException(Messages.MINIMUM_SEAT_REQUEST.value)
