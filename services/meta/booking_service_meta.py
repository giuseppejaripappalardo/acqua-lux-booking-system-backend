from abc import abstractmethod, ABC

from database.entities.booking import Booking
from models.object.token_payload import TokenPayload
from models.request.booking.booking_request import CustomerBookingRequest, EditBookingRequest


class BookingServiceMeta(ABC):
    """
    Questa classe astratta funziona come base per l'implementazione di BookingService.
    Di fatto definiamo qui i metodi che il service dovrà implementare.
    Tecnicamente fa ciò che farebbe un'interfaccia.
    """

    @abstractmethod
    def find_all(self, logged_user: TokenPayload) -> list[Booking]:
        pass

    @abstractmethod
    def make_reservation(self, reservation_data: CustomerBookingRequest, customer: TokenPayload) -> Booking:
        pass

    @abstractmethod
    def get_by_id(self, booking_id: int, customer: TokenPayload) -> Booking:
        pass

    @abstractmethod
    def edit_reservation(self, reservation_data: EditBookingRequest, customer: TokenPayload) -> Booking:
        pass

    @abstractmethod
    def delete_booking(self, logged_user: TokenPayload, booking_id: int) -> None:
        pass