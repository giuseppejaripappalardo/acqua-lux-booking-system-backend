from abc import abstractmethod, ABC

from models.request.user.user_request import UserRequest
from models.response.user.user_response import UserResponse


class UserServiceMeta(ABC):
    """
    Questa classe astratta funziona come base per l'implementazione di UserService.
    Di fatto definiamo qui i metodi che il service dovrà implementare.
    Tecnicamente fa ciò che farebbe un'interfaccia.
    """

    @abstractmethod
    def create_user(self, user: UserRequest) -> UserResponse:
        pass

    @abstractmethod
    def find_all(self):
        pass