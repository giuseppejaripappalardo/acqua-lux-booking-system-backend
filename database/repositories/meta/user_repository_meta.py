from abc import ABC

from database.entities.user import User


class UserRepositoryMeta(ABC):
    def create(self, user: User) -> User:
        pass

    def find_all(self) -> list[User]:
        pass

    def get_by_username(self, username: str) -> User | None:
        pass