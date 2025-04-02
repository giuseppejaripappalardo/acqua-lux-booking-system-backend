from abc import abstractmethod, ABC

from database.entities.boat import Boat
from models.request.booking.search_boat_request import SearchBoatRequest


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
    def find_available_boats_for_booking(self, booking_request: SearchBoatRequest, booking_id: int | None = None) -> list[Boat]:
        pass