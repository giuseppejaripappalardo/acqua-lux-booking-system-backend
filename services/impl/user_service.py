from datetime import datetime

import pytz
from fastapi import Depends

from database.entities.user import User
from database.repositories.impl.user_repository import UserRepository
from database.repositories.meta.user_repository_meta import UserRepositoryMeta
from exceptions.users.user_already_exists import UserAlreadyExists
from models.request.user.user_request import UserRequest
from models.response.user.user_response import UserResponse
from services.meta.user_service_meta import UserServiceMeta
from utils.logger_service import LoggerService
from utils.security.bcrypt_hash_password import PassowrdHasher


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
        current_timestamp = datetime.now(pytz.utc)
        new_user = User(
            username=user.username,
            password=hashed_password,
            firstname=user.firstname,
            lastname=user.lastname,
            role_id=user.role_id,
            created_at=current_timestamp,
            modified_at=current_timestamp
        )

        user_exist: User | None = self._user_repository.get_by_username(user.username)
        """
            Controllo se l'utente esiste già, se esiste lancio una eccezione specifica
            Quest'ultima verrà catturata nel main dal gestore delle eccezioni globale.
            Tecnicamente potrei farne a meno di fare il raise, perchè ci sarebbe un integrity
            constraint violation, visto che lo username è unique, ma preferisco essere specifico
            nella gestione delle eccezioni cosi da individuare subito il problema, se servisse.
        """
        if user_exist is not None:
            raise UserAlreadyExists()

        response = self._user_repository.create(new_user)
        return UserResponse.model_validate(response)


    def find_all(self) -> list[User]:
        return self._user_repository.find_all()
