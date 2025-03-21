from abc import abstractmethod, ABC

from fastapi import Response

from response.auth.auth_response import TokenResponse


class AuthServiceMeta(ABC):

    @abstractmethod
    def login(self, username: str, password: str) -> dict:
        pass

    def refresh_token(self, refresh_token: str) -> TokenResponse:
        pass