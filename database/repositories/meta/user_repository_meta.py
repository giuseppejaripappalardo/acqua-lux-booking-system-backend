from abc import ABC
from typing import Type

from database.entities import User


class UserRepositoryMeta(ABC):
    def create(self, user: User) -> User:
        pass

    def find_all(self) -> list[Type[User]]:
        pass