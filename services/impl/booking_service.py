import math
from decimal import Decimal
from uuid import uuid4

from fastapi import Depends

from database.entities.booking import Booking
from database.repositories.impl.boat_repository import BoatRepository
from database.repositories.impl.booking_repository import BookingRepository
from database.repositories.impl.user_repository import UserRepository
from database.repositories.meta.boat_repository_meta import BoatRepositoryMeta
from database.repositories.meta.booking_repository_meta import BookingRepositoryMeta
from database.repositories.meta.user_repository_meta import UserRepositoryMeta
from exceptions.base_exception import AcquaLuxBaseException
from exceptions.booking.boat_already_booked_exception import BoatAlreadyBookedException
from exceptions.booking.customer_not_found_exception import CustomerNotFoundException
from exceptions.generic.generic_not_found_exception import GenericNotFoundException
from models.object.token_payload import TokenPayload
from models.request.booking.booking_request import CustomerBookingRequest
from services.meta.booking_service_meta import BookingServiceMeta
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
            boat_repository: BoatRepositoryMeta = Depends(BoatRepository),
            user_respository: UserRepositoryMeta = Depends(UserRepository)
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
        # Metodo preposto alla validazione
        # Consultare l'implementazione per avere tutti i dettagli.
        # Se la validazione non viene superata vengono lanciate delle eccezioni
        booking_validator(reservation_data)

        self._logger_service.logger.info(f"before check")

        get_boat_to_book = self._boat_repository.get_boat_to_book(reservation_data)

        self._logger_service.logger.info(f"boat {get_boat_to_book}")

        if get_boat_to_book is None:
            self._logger_service.logger.info(f"is none so raise error")
            raise BoatAlreadyBookedException(Messages.BOAT_ALREADY_BOOKED.value)

        self._logger_service.logger.info(f"after check for {get_boat_to_book}")
        if customer is None:
            raise CustomerNotFoundException()

        price_per_hour: Decimal = get_boat_to_book.price_per_hour
        diff_hours = math.ceil((reservation_data.end_date - reservation_data.start_date).total_seconds() / 3600)
        total_amount: Decimal = price_per_hour * Decimal(diff_hours)

        reservation = Booking(
            **reservation_data.model_dump(),
            reservation_code=uuid4().hex,
            reservation_status=BookingStatuses.CONFIRMED,
            total_price=total_amount,
            customer_id=int(customer.sub),
        )

        self._logger_service.logger.info(f"customer {customer.sub}")
        self._logger_service.logger.info(f"data {reservation}")

        return self._booking_repository.make_reservation(reservation)

    def delete_booking(self, logged_user: TokenPayload, booking_id: int) -> Booking:
        booking_to_delete = self._booking_repository.get_booking(booking_id)
        if booking_to_delete is None:
            raise GenericNotFoundException()

        """
            Controllo fondamentale. Verifichiamo se la prenotazione è dell'utente che sta cercando
            di cancellarla. In caso contrario lanciamo una eccezione. Solo l'utente con ruolo
            ADMIN potrà cancellare qualsiasi prenotazione.
        """
        if  booking_to_delete.customer_id != logged_user.sub and logged_user.role != Roles.ADMIN.value:
            raise AcquaLuxBaseException(message=Messages.DELETE_OPERATION_NOT_ALLOWED.value, code=403)

        deleted = self._booking_repository.delete_booking(booking_to_delete)

        if deleted == 0:
            raise GenericNotFoundException(message=Messages.NO_BOOKINGS_DELETED.value, code=404)

        return booking_to_delete
