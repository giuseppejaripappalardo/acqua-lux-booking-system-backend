from abc import ABC

from database.entities.role import Role


class RoleRepositoryMeta(ABC):
    def find_all(self) -> list[Role]:
        pass