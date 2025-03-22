from fastapi import Depends

from database.entities.role import Role
from database.repositories.impl.role_repository import RoleRepository
from database.repositories.meta.role_repository_meta import RoleRepositoryMeta
from services.meta.role_service_meta import RoleServiceMeta
from utils.logger_service import LoggerService


class RoleService(RoleServiceMeta):
    _logger_service: LoggerService.logger = None
    _role_repository: RoleRepositoryMeta = None

    def __init__(
            self,
            logger_service: LoggerService = Depends(LoggerService),
            role_repository: RoleRepositoryMeta = Depends(RoleRepository),
    ):
        self._logger_service = logger_service
        self._role_repository = role_repository

    def find_all(self) -> list[Role]:
        return self._role_repository.find_all()