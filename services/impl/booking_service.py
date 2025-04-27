import math
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from fastapi import Depends

from database.entities.booking import Booking
from database.repositories.impl.boat_repository import BoatRepository
from database.repositories.impl.booking_repository import BookingRepository
from database.repositories.meta.boat_repository_meta import BoatRepositoryMeta
from database.repositories.meta.booking_repository_meta import BookingRepositoryMeta
from database.repositories.meta.user_repository_meta import UserRepositoryMeta
from exceptions.base_exception import AcquaLuxBaseException
from exceptions.booking.boat_already_booked_exception import BoatAlreadyBookedException
from exceptions.generic.generic_not_found_exception import GenericNotFoundException
from models.object.token_payload import TokenPayload
from models.request.booking.booking_request import CustomerBookingRequest, EditBookingRequest
from services.meta.booking_service_meta import BookingServiceMeta
from utils.datetime_provider import DateTimeProvider
from utils.enum.booking_statuses import BookingStatuses
from utils.enum.messages import Messages
from utils.enum.roles import Roles
from utils.logger_service import LoggerService
from utils.validation.booking_validator import booking_validator


class BookingService(BookingServiceMeta):
    _logger_service: LoggerService.logger = None
    _booking_repository: BookingRepositoryMeta = None
    _boat_repository: BoatRepositoryMeta = None
    _user_repository: UserRepositoryMeta = None

    def __init__(
            self,
            log_service: LoggerService = Depends(LoggerService),
            booking_repository: BookingRepositoryMeta = Depends(BookingRepository),
            boat_repository: BoatRepositoryMeta = Depends(BoatRepository)
    ):
        self._logger_service = log_service
        self._booking_repository = booking_repository
        self._boat_repository = boat_repository

    def find_all(self, logged_user: TokenPayload) -> list[Booking]:
        result = None
        if logged_user.role == Roles.ADMIN.value:
            result = self._booking_repository.find_all()
        else:
            result = self._booking_repository.find_all_for_customer(int(logged_user.sub))

        return result

    def make_reservation(self, reservation_data: CustomerBookingRequest, customer: TokenPayload) -> Booking:
        """
            Metodo preposto alla validazione
            Consultare l'implementazione per avere tutti i dettagli.
            Se la validazione non viene superata vengono lanciate delle eccezioni
        """
        booking_validator(reservation_data)

        """
            Normalizzo le date in UTC anche qui per chiarezza,
            anche se il validator già effettua le opportune verifiche e nel caso fa il cast appropriato.
        """
        reservation_data.start_date = DateTimeProvider.parse_input_datetime_to_utc(reservation_data.start_date)
        reservation_data.end_date = DateTimeProvider.parse_input_datetime_to_utc(reservation_data.end_date)

        self._logger_service.logger.info(f"before check")

        get_boat_to_book = self._boat_repository.get_boat_to_book(reservation_data)

        self._logger_service.logger.info(f"boat {get_boat_to_book}")

        """
            Se il risultato è note significa che l'imbarcazione selezionata non è disponibile.
            Restituisco un messaggio di errore informativo.
        """
        if get_boat_to_book is None:
            self._logger_service.logger.info(f"is none so raise error")
            raise BoatAlreadyBookedException(Messages.BOAT_ALREADY_BOOKED.value)

        self._logger_service.logger.info(f"after check for {get_boat_to_book}")

        self._logger_service.logger.info(f"date {reservation_data.start_date} - {reservation_data.end_date}")

        """
            Controllo se l'utente ha già prenotazioni nello stesso range temporale per cui intende prenotare.
            In caso positivo lancio una eccezione. Per scelta di progettazione non consento prenotazioni simultanee.
        """
        check_customer_existing_booking = self._booking_repository.check_customer_existing_bookings(int(customer.sub),
                                                                                                    reservation_data.start_date,
                                                                                                    reservation_data.end_date)
        if check_customer_existing_booking:
            self._logger_service.logger.info(f"Cliente {customer.sub} ha già una prenotazione per questo periodo")
            raise BoatAlreadyBookedException(Messages.CUSTOMER_ALREADY_HAS_BOOKING.value)

        price_per_hour: Decimal = get_boat_to_book.price_per_hour
        diff_hours = math.ceil((reservation_data.end_date - reservation_data.start_date).total_seconds() / 3600)
        total_amount: Decimal = price_per_hour * Decimal(diff_hours)
        current_timestamp = datetime.now(timezone.utc)

        reservation = Booking(
            **reservation_data.model_dump(),
            reservation_code=uuid4().hex,
            reservation_status=BookingStatuses.CONFIRMED,
            total_price=total_amount,
            customer_id=int(customer.sub),
            created_at=current_timestamp,
            modified_at=current_timestamp
        )

        self._logger_service.logger.info(f"customer {customer.sub}")
        self._logger_service.logger.info(f"data {reservation}")

        return self._booking_repository.make_reservation(reservation)

    def edit_reservation(self, reservation_data: EditBookingRequest, customer: TokenPayload) -> Booking:
        reservation_to_edit = self._booking_repository.get_booking(reservation_data.booking_id)

        """
            Controlliamo se la prenotazione da modificare esiste.
            Se non esiste lancio una eccezione con http code 404.
        """
        if reservation_to_edit is None:
            self._logger_service.logger.info(f"Stiamo cercando di modificare una prenotazione che non esiste.")
            raise GenericNotFoundException(message=Messages.BOOKING_TO_EDIT_NOT_FOUND.value, code=404)

        """
            Ci assicuriamo qui che il tentativo di modifica prenotazione viene fatto dall'utente che ha effettuato la prenotazione.
            Se l'id dell'utente autenticato non coincide con l'id del customer significa che stiamo
            tentando di fare la prenotazione per qualcun'altro. Questa operazione sarà consentita solo 
            se avviene da parte di un utente con ruolo ADMIN.
            
            NOTA: poichè customer.role arriva dal TokenPayload il controllo deve necessariamente essere fatto con
            Roles.ADMIN.value per confrontare due stringhe.
        """
        if int(reservation_to_edit.customer_id) != int(customer.sub) and customer.role != Roles.ADMIN.value:
            self._logger_service.logger.info(
                "Attenzione, un utente sta cercando di modificare la prenotazione di un altro utente.")
            raise AcquaLuxBaseException(message=Messages.BOOKING_CUSTOMER_ONLY.value, code=403)

        """
            Controllo se lo stato è incompatibile con la modifica.
            Al momento prevedo che soltanto le prenotazioni confermate possono
            essere modificate.
        """
        if reservation_to_edit.reservation_status != BookingStatuses.CONFIRMED:
            raise AcquaLuxBaseException(message=Messages.BOOKING_EDIT_INCOMPATIBLE_STATE.value, code=422)

        """
            A questo punto un aspetto molto importante da verificare è quello di capire se si sta cercando di modificare una prenotazione già in corso.
            Di base per semplificare le logiche, assumo che una prenotazione in corso non può più essere modificata.
            Quindi se start_date è maggiore della current date allora non possiamo consentire la modifica. Vuol dire che il charter è già in corso.
            Faremo il controllo del datetime now in UTC, visto che come indicato anche in altri punti, tutte le date a DB sono salvate in UTC.
        """
        current_date = datetime.now(timezone.utc)
        start_date = DateTimeProvider.parse_input_datetime_to_utc(reservation_to_edit.start_date)
        self._logger_service.logger.info(
            f"START DATE ORIGINALE: {reservation_to_edit.start_date} - tz: {reservation_to_edit.start_date.tzinfo}")
        self._logger_service.logger.info(f"START DATE UTC: {start_date}")
        self._logger_service.logger.info(f"CURRENT UTC: {current_date}")
        if start_date <= current_date:
            raise AcquaLuxBaseException(message=Messages.BOOKING_MODIFICATION_NOT_ALLOWED.value, code=422)

        """
            Verifico se effettivamente è stata cambiata anche l'imbarcazione.
        """
        boat_is_changed = reservation_to_edit.boat_id != reservation_data.boat_id

        """
            Costruisco il modello di dati necessario. Mi serve usare questo Type
            Perchè possiamo sfruttare il polimorfismo con il validator che fa diversi controlli
            sulla validità delle date previste per la prenotazione. Considerato che si tratta di una modifica
            non possiamo dare nulla per scontato e gli stessi controlli previsti in fase di inserimento prenotazione
            andranno rifatti in questa sede.
        """
        edited_reservation = CustomerBookingRequest(
            start_date=reservation_data.start_date,
            end_date=reservation_data.end_date,
            boat_id=reservation_data.boat_id if boat_is_changed else reservation_to_edit.boat_id,
            payment_method=reservation_to_edit.payment_method,
            notes=reservation_data.notes,
            seat=reservation_data.seat,
        )

        """
            A questo punto prima pocedere con qualsiasi operazione chiamo il validator,
            per verificare se i dati input che ho ricevuto sono conformi alle regole di validazione previste.
        """
        booking_validator(edited_reservation)

        """
            Se siamo arrivati fin qui ora dobbiamo controllare se l'imbarcazione è stata modificata.
            Se è stata modificata allora dobbiamo capire se è effettivamente disponibile.
        """
        get_boat_to_book = self._boat_repository.get_boat_to_book(edited_reservation, int(customer.sub))

        if get_boat_to_book is None:
            self._logger_service.logger.info(
                f"L'imbarcazione che è stata scelta per la modifica non è disponibile. Non è possibile procedere con questa operazione.")
            raise BoatAlreadyBookedException(Messages.BOAT_ALREADY_BOOKED.value)

        """
            Prendiamo il costo totale della prenotazione da modificare.
        """
        old_total = reservation_to_edit.total_price

        """
            Calcoliamo qui il nuovo costo totale della prenotazione.
            Prendiamo la data di fine - la data di inizio e la dividiamo per 3600 per ottenere il numero di ore.
            Infine basterà moltiplicare il numero di ore per il costo orario della nuova imbarcazione.
        """
        diff_hours = math.ceil((reservation_data.end_date - reservation_data.start_date).total_seconds() / 3600)
        new_price_per_hour = get_boat_to_book.price_per_hour
        new_total = new_price_per_hour * Decimal(diff_hours)

        """
            A questo punto possiamo calcolare la differenza.
        """
        price_difference = new_total - old_total
        refund = price_difference < 0

        current_timestamp = datetime.now(timezone.utc)

        """
            Se siamo arrivati fin qui abbiamo superato tutti i controlli. Significa che possiamo costruire il modello
            per persisterlo nel database. Manteniamo il reservation_code visto che comunque si tratta di una modifica
            di una prenotazione esistente.
        """
        reservation_to_edit.seat = edited_reservation.seat
        reservation_to_edit.start_date = edited_reservation.start_date
        reservation_to_edit.end_date = edited_reservation.end_date
        reservation_to_edit.boat_id = edited_reservation.boat_id
        reservation_to_edit.notes = edited_reservation.notes
        reservation_to_edit.total_price = new_total
        reservation_to_edit.price_difference = price_difference
        reservation_to_edit.requires_refund = refund
        reservation_to_edit.modified_at = current_timestamp

        return self._booking_repository.edit_reservation(reservation_to_edit)

    def delete_booking(self, logged_user: TokenPayload, booking_id: int) -> Booking:
        """
            Prima di eseguire qualsiasi operazione mi assicuro che la prenotazione che si vuole cancellare
            esista, altrimenti lanciamo un eccezione.
        """
        booking_to_delete = self._booking_repository.get_booking(booking_id)
        if booking_to_delete is None:
            raise GenericNotFoundException()

        """
            Controllo fondamentale. Verifichiamo se la prenotazione è dell'utente che sta cercando
            di cancellarla. In caso contrario lanciamo una eccezione. Solo l'utente con ruolo
            ADMIN potrà cancellare qualsiasi prenotazione.
        """
        if int(booking_to_delete.customer_id) != int(logged_user.sub) and logged_user.role != Roles.ADMIN.value:
            self._logger_service.logger.info(
                "Attenzione, un utente sta cercando di modificare la prenotazione di un altro utente.")
            raise AcquaLuxBaseException(message=Messages.DELETE_OPERATION_NOT_ALLOWED.value, code=403)

        """
            Verifichiamo se la prenotazione è cancellabile.
            Se è già stata cancellata allora dobbiamo informare l'utente
            e non fare nessuna azione. Qui è sicuro dare un messaggio specifico
            perchè sopra, stiamo controllando se l'utente che cancella è l'utente autenticato ovvero
            colui che ha fatto la prenotazione. Quindi non stiamo fornendo dati sensitivi.
        """
        if booking_to_delete.reservation_status == BookingStatuses.CANCELLED:
            raise AcquaLuxBaseException(message=Messages.BOOKING_ALREADY_DELETED.value, code=422)

        """
            A questo punto un aspetto molto importante da verificare è quello di capire se si sta cercando di modificare una prenotazione già in corso.
            Di base per semplificare le logiche, assumo che una prenotazione in corso non può più essere modificata.
            Quindi se start_date è maggiore della current date allora non possiamo consentire la cancellazione. Vuol dire che il charter è già in corso.
            Faremo il controllo del datetime now in UTC, visto che come indicato anche in altri punti, tutte le date a DB sono salvate in UTC.
        """
        current_date = datetime.now(timezone.utc)
        start_date = DateTimeProvider.parse_input_datetime_to_utc(booking_to_delete.start_date)

        """
            Se la data di inizio è minore o uguale alla data corrente allora lanciamo l'eccezione
            e non consentiamo il soft delete.
        """
        if start_date <= current_date:
            raise AcquaLuxBaseException(message=Messages.BOOKING_MODIFICATION_NOT_ALLOWED.value, code=422)

        """
            Se abbiamo superato tutti i controlli a questo punto aggiorniamo lo stato
            in CANCELLED e aggiorniamo la data di modifica per tracciare l'operazione.
        """
        booking_to_delete.reservation_status = BookingStatuses.CANCELLED
        booking_to_delete.modified_at = current_date
        return self._booking_repository.delete_booking(booking_to_delete)

    def get_by_id(self, booking_id: int, customer: TokenPayload) -> Booking:
        booking: Booking = self._booking_repository.get_booking(booking_id)

        if int(booking.customer_id) != int(customer.sub) and customer.role != Roles.ADMIN.value:
            raise AcquaLuxBaseException(message=Messages.GET_BOOKING_CUSTOMER_ONLY.value, code=403)

        if booking is None:
            raise GenericNotFoundException(message=Messages.NOT_FOUND.value, code=404)

        if booking.reservation_status != BookingStatuses.CONFIRMED:
            raise AcquaLuxBaseException(message=Messages.BOOKING_EDIT_INCOMPATIBLE_STATE.value, code=422)

        return booking
