from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import Database
from database.entities.user import User
from models.user import UserOut

router = APIRouter(prefix="/user", tags=["user"])
db = Database()

@router.get("/", response_model=List[UserOut])
def users_list(db_session: Session = Depends(db.get_db)):
    return db_session.query(User).all()
