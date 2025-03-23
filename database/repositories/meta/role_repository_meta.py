from abc import ABC, abstractmethod

from database.entities.role import Role


class RoleRepositoryMeta(ABC):

    @abstractmethod
    def find_all(self) -> list[Role]:
        pass