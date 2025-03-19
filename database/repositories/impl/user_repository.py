from fastapi import Depends
from sqlalchemy.orm import Session

from config.database import Database
from database.repositories.meta.user_repository_meta import UserRepositoryMeta
from database.entities import User


class UserRepository(UserRepositoryMeta):

    _db: Session = None

    def __init__(self, db: Session = Depends(Database().get_db)):
        self._db = db

    def create(self, user: User):
        print(user)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
