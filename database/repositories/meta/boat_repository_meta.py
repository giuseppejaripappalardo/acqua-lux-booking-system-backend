from abc import ABC

from database.entities.boat import Boat
from models.request.booking.booking_request import BookingRequest


class BoatRepositoryMeta(ABC):
    def find_all(self) -> list[Boat]:
        pass

    def find_available_boats_for_booking(self, booking_request: BookingRequest) -> list[Boat]:
        pass