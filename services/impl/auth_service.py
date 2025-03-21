from fastapi import Depends, Response
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from exceptions.auth.auth_exception import AuthException
from exceptions.base_exception import AcquaLuxBaseException
from exceptions.generic.generic_database_exceptionen import GenericDatabaseException
from exceptions.generic.integrity_database_exception import IntegrityDatabaseException
from models.request.auth.auth_request import LoginRequest
from utils.jwt_utils import JwtUtils
from utils.logger_service import LoggerService
from services.meta.auth_service_meta import AuthServiceMeta
from database.repositories.impl.user_repository import UserRepository
from models.response.auth.auth_response import TokenResponse
from utils.bcrypt_hash_password import PassowrdHasher
from utils.messages import Messages


class AuthService(AuthServiceMeta):
    _logger_service = None
    _user_repository = None

    def __init__(self, logger_service: LoggerService = Depends(LoggerService),
                 user_repository: UserRepository = Depends(UserRepository)):
        self._logger_service = logger_service
        self._user_repository = user_repository

    def login(self, login: LoginRequest) -> TokenResponse:
        try:
            user = self._user_repository.get_by_username(login.username)

            if user is None or PassowrdHasher().bscript_verify_password(login.password, user.password) is False:
                self._logger_service.logger.error("Invalid username or password")
                raise AuthException("Invalid username or password")
            payload = {"sub": str(user.id), "role": user.role.name}
            # "cookie_info": {
            #     "key": "refresh_token",
            #     "value": self._jwt_utils.create_refresh_token(payload),
            # }
            return TokenResponse(
                jwt_token=JwtUtils.create_access_token(payload)
            )
        except IntegrityError as e:
            self._logger_service.logger.info(f"Constraint violati: {e}")
            raise IntegrityDatabaseException(table_name="users")
        except AuthException as e:
            raise AuthException(message=e.message, code=e.code)
        except Exception as e:
            self._logger_service.logger.info(f"{Messages.GENERIC_DATABASE_ERROR.value} {e}")
            raise AcquaLuxBaseException(message=Messages.GENERIC_DATABASE_ERROR.value, code=500) from e


    def refresh_token(self, refresh_token: str) -> TokenResponse:
        try:
            payload = JwtUtils.decode_token(refresh_token)
        except Exception as e:
            self._logger_service.logger.error(f"Error decoding token: {e}")
            raise AuthException("Invalid refresh token")

        new_payload = {"sub": payload["sub"], "role": payload["role"]}

        return TokenResponse(
            jwt_token=JwtUtils.create_access_token(new_payload),
            refresh_token=JwtUtils.create_refresh_token(new_payload)
        )