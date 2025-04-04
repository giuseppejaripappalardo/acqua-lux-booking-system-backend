from abc import ABC, abstractmethod

from database.entities.role import Role


class RoleServiceMeta(ABC):
    """
        Questa classe astratta funziona come base per l'implementazione di RoleService.
        Di fatto definiamo qui i metodi che il service dovrà implementare.
        Tecnicamente fa ciò che farebbe un'interfaccia.
    """

    @abstractmethod
    def find_all(self) -> list[Role]:
        pass
