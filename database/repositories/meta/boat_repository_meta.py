from abc import ABC, abstractmethod

from database.entities.boat import Boat
from models.request.booking.search_boat_request import SearchBoatRequest


class BoatRepositoryMeta(ABC):

    @abstractmethod
    def find_all(self) -> list[Boat]:
        pass

    @abstractmethod
    def find_available_boats_for_booking(self, booking_request: SearchBoatRequest) -> list[Boat]:
        pass

    @abstractmethod
    def get_boat_to_book(self, booking_request: SearchBoatRequest) -> Boat:
        pass