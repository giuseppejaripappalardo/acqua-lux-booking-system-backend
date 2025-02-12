from typing import List

import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.user import User
from schemas.user import UserOut, UserCreate

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # usiamo bcrypt per far si che la password venga cifrata
    # l'encode lo faccio con utf-8 con lo scopo di garantire un set ampio di caratteri.
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(
        username=user.username,
        password=hashed_password,
        firstname=user.firstname,
        lastname=user.lastname,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
