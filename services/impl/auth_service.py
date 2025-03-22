from fastapi import Depends

from database.entities.user import User
from database.repositories.impl.user_repository import UserRepository
from exceptions.auth.auth_exception import AuthException
from models.request.auth.auth_request import LoginRequest
from models.response.auth.auth_response import TokenResponse
from services.meta.auth_service_meta import AuthServiceMeta
from utils.bcrypt_hash_password import PassowrdHasher
from utils.jwt_utils import JwtUtils
from utils.logger_service import LoggerService


class AuthService(AuthServiceMeta):
    _logger_service = None
    _user_repository = None

    def __init__(self, logger_service: LoggerService = Depends(LoggerService),
                 user_repository: UserRepository = Depends(UserRepository)):
        self._logger_service = logger_service
        self._user_repository = user_repository

    def login(self, login: LoginRequest) -> TokenResponse:
        user: User = self._user_repository.get_by_username(login.username)

        if user is None or PassowrdHasher().bscript_verify_password(login.password, user.password) is False:
            self._logger_service.logger.error("Invalid username or password")
            raise AuthException("Invalid username or password")
        payload = {"sub": str(user.id), "role": user.role.name}
        return TokenResponse(
            jwt_token=JwtUtils.create_access_token(payload)
        )