from abc import abstractmethod, ABC

from models.request.auth.auth_request import LoginRequest
from models.response.auth.auth_response import TokenResponse


class AuthServiceMeta(ABC):

    @abstractmethod
    def login(self, login: LoginRequest) -> TokenResponse:
        pass

    def refresh_token(self, refresh_token: str) -> TokenResponse:
        pass