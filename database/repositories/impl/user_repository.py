from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.user import User
from database.repositories.meta.user_repository_meta import UserRepositoryMeta


class UserRepository(UserRepositoryMeta):
    _db: Session = None

    def __init__(self, db: Session = Depends(Database().get_db)):
        self._db = db

    def create(self, user: User) -> User:
        self._db.add(user)
        self._db.commit()
        self._db.flush()
        return user

    def find_all(self) -> list[User]:
        stmt = select(User)
        return list(self._db.scalars(stmt))

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self._db.scalars(stmt).first()
