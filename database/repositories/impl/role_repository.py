from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.role import Role
from database.repositories.meta.role_repository_meta import RoleRepositoryMeta


class RoleRepository(RoleRepositoryMeta):

    _db: Session = None

    def __init__(self, db: Session = Depends(Database().get_db)):
        self._db = db

    def find_all(self) -> list[Role]:
        stmt = select(Role)
        return list(self._db.scalars(stmt))