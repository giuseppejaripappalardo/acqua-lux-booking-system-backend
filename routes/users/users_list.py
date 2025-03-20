from typing import List

from fastapi import APIRouter, Depends

from config.database import Database
from controllers.user_controller import UserController
from response.user.user_response import UserResponse

router = APIRouter(prefix="/user", tags=["user"])
db = Database()

@router.get("/", response_model=List[UserResponse])
def users_list(user_controller: UserController = Depends(UserController)):
    return user_controller.find_all()
