from fastapi import Depends, Response

from exceptions.auth.auth_exception import AuthException
from jwt_utils import JwtUtils
from logger_service import LoggerService
from meta.auth_service_meta import AuthServiceMeta
from repositories.impl.user_repository import UserRepository
from response.auth.auth_response import TokenResponse
from bcrypt_hash_password import PassowrdHasher


class AuthService(AuthServiceMeta):
    _logger_service = None
    _user_repository = None
    _jwt_utils = None

    def __init__(self, logger_service: LoggerService = Depends(LoggerService),
                 user_repository: UserRepository = Depends(UserRepository)):
        self._logger_service = logger_service
        self._user_repository = user_repository
        self._jwt_utils = JwtUtils()

    def login(self, username: str, password: str) -> dict:
        user = self._user_repository.get_by_username(username)

        if user is None or PassowrdHasher().bscript_verify_password(password, user.password) is False:
            self._logger_service.logger.error("Invalid username or password")
            raise AuthException("Invalid username or password")
        payload = {"sub": str(user.id), "role": user.role.name}
        return {
            "token_data": TokenResponse(
                jwt_token=self._jwt_utils.create_access_token(payload),
                refresh_token=self._jwt_utils.create_refresh_token(payload)
            ),
            "cookie_info": {
                "key": "refresh_token",
                "value": self._jwt_utils.create_refresh_token(payload),
            }
        }

    def refresh_token(self, refresh_token: str) -> TokenResponse:

        try:
            payload = self._jwt_utils.decode_token(refresh_token)
        except Exception as e:
            self._logger_service.logger.error(f"Error decoding token: {e}")
            raise AuthException("Invalid refresh token")

        new_payload = {"sub": payload["sub"], "role": payload["role"]}

        return TokenResponse(
            jwt_token=self._jwt_utils.create_access_token(new_payload),
            refresh_token=self._jwt_utils.create_refresh_token(new_payload)
        )
