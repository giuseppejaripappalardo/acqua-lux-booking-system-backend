import bcrypt
from fastapi import Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from database.repositories.impl.user_repository import UserRepository
from database.repositories.meta.user_repository_meta import UserRepositoryMeta
from database.entities import User
from logger_service import LoggerService
from models.user import UserCreate, UserOut
from services.meta.user_service_meta import UserServiceMeta


class UserService(UserServiceMeta):

    _logger_service: LoggerService.logger = None
    _user_repository: UserRepositoryMeta = None

    def __init__(self, log_service: LoggerService = Depends(LoggerService), user_repository: UserRepositoryMeta = Depends(UserRepository)):
        self._logger_service = log_service
        self._user_repository = user_repository

    def create_user(self, user: UserCreate) -> UserOut:
        try:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(
                username=user.username,
                password=hashed_password,
                firstname=user.firstname,
                lastname=user.lastname,
                role_id=1
            )
            return self._user_repository.create(new_user)
        except IntegrityError as e:
            self._logger_service.logger.info(f"Constraint violati: {e}")
            raise HTTPException(status_code=400, detail="Violazione dei vincoli di integrità") from e
        except SQLAlchemyError as e:
            self._logger_service.logger.info(f"Si è verificato un errore nel database {e}")
            raise HTTPException(status_code=500, detail="Si è verificato un errore nel database") from e
        except Exception as e:
            self._logger_service.logger.info(f"Si è verificato un errore imprevisto {e}")
            raise Exception("Si è verificato un errore imprevisto") from e
