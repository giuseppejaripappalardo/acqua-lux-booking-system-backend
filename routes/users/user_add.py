from fastapi import APIRouter, Depends

from controllers.user_controller import UserController
from request.user.user_request import UserRequest
from response.user.user_response import UserResponse

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=UserResponse)
def user_add(user: UserRequest, user_controller: UserController = Depends(UserController)):
    return user_controller.create_user(user)