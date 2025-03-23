from abc import ABC

from database.entities.booking import Booking


class BookingRepositoryMeta(ABC):
    def find_all(self) -> list[Booking]:
        pass