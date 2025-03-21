from typing import List

from fastapi import APIRouter, Depends

from controllers.user_controller import UserController
from request.user.user_request import UserRequest
from response.user.user_response import UserResponse

router = APIRouter()

@router.post("/create", response_model=UserResponse)
async def user_add(user: UserRequest, user_controller: UserController = Depends(UserController)):
    return await user_controller.create_user(user)

@router.get("/list", response_model=List[UserResponse])
async def users_list(user_controller: UserController = Depends(UserController)):
    return await user_controller.find_all()