from abc import ABC, abstractmethod

from database.entities.booking import Booking
from models.request.booking.booking_request import CustomerBookingRequest


class BookingRepositoryMeta(ABC):

    @abstractmethod
    def find_all(self) -> list[Booking]:
        pass

    @abstractmethod
    def make_reservation(self, reservation_data: Booking) -> Booking:
        pass