from abc import abstractmethod, ABC

from database.entities.boat import Boat
from models.request.booking.booking_request import BookingRequest


class BoatServiceMeta(ABC):
    """
    Questa classe astratta funziona come base per l'implementazione di BoatService.
    Di fatto definiamo qui i metodi che il service dovrà implementare.
    Tecnicamente fa ciò che farebbe un'interfaccia.
    """

    @abstractmethod
    def find_all(self) -> list[Boat]:
        pass

    @abstractmethod
    def find_available_boats_for_booking(self, booking_request: BookingRequest) -> list[Boat]:
        pass