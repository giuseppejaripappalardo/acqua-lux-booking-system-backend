from abc import ABC

from database.entities import User


class UserRepositoryMeta(ABC):
    def create(self, user: User):
        pass