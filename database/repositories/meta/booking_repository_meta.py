from abc import ABC, abstractmethod

from database.entities.booking import Booking
from models.request.booking.booking_request import CustomerBookingRequest


class BookingRepositoryMeta(ABC):

    @abstractmethod
    def find_all(self) -> list[Booking]:
        pass

    @abstractmethod
    def find_all_for_customer(self, customer_id: int) -> list[Booking]:
        pass

    @abstractmethod
    def make_reservation(self, reservation_data: Booking) -> Booking:
        pass

    @abstractmethod
    def delete_booking(self, booking: Booking) -> int:
        pass

    @abstractmethod
    def get_booking(self, booking_id: int) -> Booking | None:
        pass