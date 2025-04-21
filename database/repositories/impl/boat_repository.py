from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.boat import Boat
from database.entities.boat_statuses import BoatStatuses
from database.entities.booking import Booking
from database.repositories.meta.boat_repository_meta import BoatRepositoryMeta
from models.request.booking.search_boat_request import SearchBoatRequest
from utils.enum.boat_statuses_values import BoatStatusesValues
from utils.enum.booking_statuses import BookingStatuses
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

    def find_available_boats_for_booking(self, booking_request: SearchBoatRequest,
                                         existing_booking_id: int | None = None) -> list[Boat]:

        conditions = [
            Booking.boat_id == Boat.id,
            Booking.start_date < booking_request.end_date,
            Booking.end_date > booking_request.start_date,
            Booking.reservation_status == BookingStatuses.CONFIRMED
        ]


        """
            Questo metodo riceve existing_booking_id solo nel caso in cui si stia modificando una prenotazione.
            La modifica implica la verifica delle disponibilità e questo controllo è essenziale per escludere 
            l'imbarcazione presente nella prenotazione che stiamo modificando. Ad esempio il cliente potrebbe
            voler modificare soltanto le date e scegliere comunque la stessa imbarcazione.
        """
        if existing_booking_id is not None:
            conditions.append(Booking.id != existing_booking_id)

        search_terms = and_(
            *conditions
        )

        stmt = (
            select(Boat)
            .join(BoatStatuses)
            .outerjoin(
                Booking,
                search_terms
            )
            .where(
                BoatStatuses.name == BoatStatusesValues.AVAILABLE,
                Boat.seat >= booking_request.seat,
                # Nessun booking in conflitto
                Booking.id.is_(None)
            )
        )
        return list(self._db.scalars(stmt))

    def get_boat_to_book(self, booking_request: SearchBoatRequest, booking_id: int = None) -> Boat:
        """
        Queste condizioni servono a verificare se ci sono sovrapposizioni tra la prenotazione
        richiesta e altre prenotazioni esistenti.
        In pratica, sto cercando qualsiasi prenotazione confermata per la stessa barca
        che si sovrapponga al periodo richiesto. Una sovrapposizione avviene quando:
        - Si tratta della stessa barca che si sta cercando di prenotare
        - Il periodo della prenotazione esistente (ovvero una prenotazione) si sovrappone in qualche modo
          con il periodo richiesto
        - La prenotazione è confermata (escludo volutamente quelle in stato CANCELLED)
        """
        booking_overlap_condition = and_(
            Booking.boat_id == Boat.id,
            Booking.start_date < booking_request.end_date,
            Booking.end_date > booking_request.start_date,
            Booking.reservation_status == BookingStatuses.CONFIRMED
        )

        """
            Quando viene fornito un booking_id per la modifica, escludiamo le prenotazioni di questo cliente 
            dal controllo di conflitti solo per il booking che si sta modificando. 
            Questo perché un cliente deve poter modificare la propria prenotazione senza che il sistema la consideri come "già occupata".
            Esempio (se il cliente ha già prenotato una barca e vuole cambiare le date)
        """
        if booking_id is not None:
            booking_overlap_condition = and_(
                booking_overlap_condition,
                Booking.id != booking_id
            )

        """
            Con questa query cerco una barca che:
            - È disponibile secondo lo stato generale del sistema
            - Ha abbastanza posti per le persone richieste
            - Corrisponde alla barca specifica richiesta dal cliente
            - Non ha sovrapposizioni con altre prenotazioni nel periodo desiderato
              (questo è garantito dalla condizione Booking.id.is_(None) combinata
              con l'outerjoin che abbiamo definito sopra)
        """
        stmt_boat = (select(Boat)
            .join(BoatStatuses)
            .outerjoin(Booking, booking_overlap_condition)
            .where(
                BoatStatuses.name == BoatStatusesValues.AVAILABLE,
                Boat.seat >= booking_request.seat,
                Boat.id == booking_request.boat_id,
                Booking.id.is_(None)
            )
        )
        return self._db.scalar(stmt_boat)
