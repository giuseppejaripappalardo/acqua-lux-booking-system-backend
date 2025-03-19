from abc import abstractmethod, ABC

from models.user import UserCreate, UserOut


class UserServiceMeta(ABC):

    @abstractmethod
    def create_user(self, user: UserCreate) -> UserOut:
        pass