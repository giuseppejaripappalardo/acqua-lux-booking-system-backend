from abc import ABC, abstractmethod
from datetime import datetime

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
    def edit_reservation(self, reservation_data: Booking) -> Booking:
        pass

    @abstractmethod
    def check_customer_existing_bookings(self, customer_id: int, start_date: datetime, end_date: datetime) -> bool:
        pass

    @abstractmethod
    def delete_booking(self, booking: Booking) -> Booking:
        pass

    @abstractmethod
    def get_booking(self, booking_id: int) -> Booking | None:
        pass