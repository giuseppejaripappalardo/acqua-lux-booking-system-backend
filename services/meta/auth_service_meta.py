from abc import abstractmethod, ABC

from exceptions.base_exception import AcquaLuxBaseException
from models.request.auth.auth_request import LoginRequest
from models.response.auth.auth_response import TokenResponse
from fastapi import Response, Request


class AuthServiceMeta(ABC):
    """
        Questa classe astratta funziona come base per l'implementazione di AuthService.
        Di fatto definiamo qui i metodi che il service dovrà implementare.
        Tecnicamente fa ciò che farebbe un'interfaccia.
    """

    @abstractmethod
    def login(self, response: Response, login: LoginRequest) -> TokenResponse:
        pass

    @abstractmethod
    def refresh(self, request: Request) -> TokenResponse:
        pass

    @abstractmethod
    def logout(self, request: Request, response: Response) -> None:
        pass
