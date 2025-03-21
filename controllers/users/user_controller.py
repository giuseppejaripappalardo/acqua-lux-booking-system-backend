from fastapi import APIRouter, Depends, Request

from models.request.user.user_request import UserRequest
from models.response.base_response import BaseResponse
from models.response.user.user_response import UserResponse
from services.impl.user_service import UserService
from services.meta.user_service_meta import UserServiceMeta
from utils.auth_cheker import AuthChecker
from utils.format_response import success_response

router = APIRouter()

@router.post("/create", response_model=BaseResponse[UserResponse])
def user_add(user: UserRequest,user_service: UserServiceMeta = Depends(UserService)) -> BaseResponse[UserResponse]:
    return success_response(user_service.create_user(user))

@router.get("/list", response_model=BaseResponse[list[UserResponse]])
def users_list(request: Request, user_service: UserServiceMeta = Depends(UserService), ) -> BaseResponse[list[UserResponse]]:
    user = AuthChecker.assert_has_role(request, ["CUSTOMER"])
    return success_response(user_service.find_all())