from abc import abstractmethod, ABC

from database.entities.booking import Booking


class BookingServiceMeta(ABC):
    """
    Questa classe astratta funziona come base per l'implementazione di BookingService.
    Di fatto definiamo qui i metodi che il service dovrà implementare.
    Tecnicamente fa ciò che farebbe un'interfaccia.
    """

    @abstractmethod
    def find_all(self) -> list[Booking]:
        pass