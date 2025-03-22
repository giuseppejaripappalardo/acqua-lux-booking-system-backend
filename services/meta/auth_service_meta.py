from abc import abstractmethod, ABC

from models.request.auth.auth_request import LoginRequest
from models.response.auth.auth_response import TokenResponse


class AuthServiceMeta(ABC):
    """
        Questa classe astratta funziona come base per l'implementazione di AuthService.
        Di fatto definiamo qui i metodi che il service dovrà implementare.
        Tecnicamente fa ciò che farebbe un'interfaccia.
    """
    @abstractmethod
    def login(self, login: LoginRequest) -> TokenResponse:
        pass