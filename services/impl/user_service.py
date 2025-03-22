from typing import Type

from fastapi import Depends

from database.entities.user import User
from database.repositories.impl.user_repository import UserRepository
from database.repositories.meta.user_repository_meta import UserRepositoryMeta
from models.request.user.user_request import UserRequest
from models.response.user.user_response import UserResponse
from services.meta.user_service_meta import UserServiceMeta
from utils.bcrypt_hash_password import PassowrdHasher
from utils.logger_service import LoggerService


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
        hashed_password = PassowrdHasher().bcrypt_hash_password(user.password)
        new_user = User(
            username=user.username,
            password=hashed_password,
            firstname=user.firstname,
            lastname=user.lastname,
            role_id=1
        )
        response = self._user_repository.create(new_user)
        return UserResponse.model_validate(response)


    def find_all(self) -> list[User]:
        raw_response: list[User] = self._user_repository.find_all()

        """
            Sto usando list comprehension per evitare un ciclo standard.
            Lo scopo è quello di chiamare il model_validate su ogni elemento.
            Cosi pydantic farà il parse per validare i dati restituiti da SQL Alchemy.
        """
        #parsed_response: list[UserResponse] = [UserResponse.model_validate(user) for user in raw_response]
        return raw_response
