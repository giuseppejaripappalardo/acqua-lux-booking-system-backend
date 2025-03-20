from typing import Type

import bcrypt
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from database.repositories.impl.user_repository import UserRepository
from database.repositories.meta.user_repository_meta import UserRepositoryMeta
from database.entities import User
from exceptions.generic.GenericDatabaseException import GenericDatabaseException
from exceptions.generic.IntegrityDatabaseException import IntegrityDatabaseException
from logger_service import LoggerService
from messages import Messages
from response.user.user_response import UserResponse
from request.user.user_request import UserRequest
from services.meta.user_service_meta import UserServiceMeta


class UserService(UserServiceMeta):
    _logger_service: LoggerService.logger = None
    _user_repository: UserRepositoryMeta = None

    def __init__(self, log_service: LoggerService = Depends(LoggerService),
                 user_repository: UserRepositoryMeta = Depends(UserRepository)):
        self._logger_service = log_service
        self._user_repository = user_repository

    def create_user(self, user: UserRequest) -> UserResponse:
        """
            Metodo preposto del service per la creazione degli utenti.
        """
        try:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(
                username=user.username,
                password=hashed_password,
                firstname=user.firstname,
                lastname=user.lastname,
                role_id=1
            )
            response = self._user_repository.create(new_user)
            return UserResponse.model_validate(response)
        except IntegrityError as e:
            self._logger_service.logger.info(f"Constraint violati: {e}")
            raise IntegrityDatabaseException(table_name="users")
        except SQLAlchemyError as e:
            self._logger_service.logger.info(f"{Messages.GENERIC_DATABASE_ERROR.value} {e}")
            raise GenericDatabaseException(message=Messages.GENERIC_DATABASE_ERROR.value) from e

    def find_all(self) -> list[UserResponse]:
        try:
            raw_response: list[Type[User]] = self._user_repository.find_all()

            """
                Sto usando list comprehension per evitare un ciclo standard.
                Lo scopo è quello di chiamare il model_validate su ogni elemento.
                Cosi pydantic farà il parse per validare i dati restituiti da SQL Alchemy.
            """
            parsed_response: list[UserResponse] = [UserResponse.model_validate(user) for user in raw_response]
            return parsed_response
        except SQLAlchemyError as e:
            self._logger_service.logger.info(f"{Messages.GENERIC_DATABASE_ERROR.value} {e}")
            raise GenericDatabaseException(message=Messages.GENERIC_DATABASE_ERROR.value) from e
