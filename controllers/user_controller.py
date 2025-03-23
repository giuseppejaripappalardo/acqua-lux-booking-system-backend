from fastapi import APIRouter, Depends, Request

from models.request.user.user_request import UserRequest
from models.response.base_response import BaseResponse
from models.response.user.user_response import UserResponse
from services.impl.user_service import UserService
from services.meta.user_service_meta import UserServiceMeta
from utils.auth_checker import AuthChecker
from utils.format_response import success_response
from utils.roles import Roles

router = APIRouter()

@router.post(
    "/add",
    response_model=BaseResponse[UserResponse],
    summary="Questo endpoint permette di creare un nuovo utente nel sistema.",
    description="Fornisce la possibilità di aggiungere un nuovo utente fornendo i dati necessari."
)
async def user_add(request: Request, user: UserRequest, user_service: UserServiceMeta = Depends(UserService)) -> BaseResponse[UserResponse]:
    AuthChecker.assert_has_role(request, [Roles.ADMIN.value])
    return success_response(user_service.create_user(user))

@router.get(
    "/list",
    response_model=BaseResponse[list[UserResponse]],
    summary="Mostra la lista di tutti gli utenti registrati",
    description="Recupera e restituisce un elenco di tutti gli utenti registrati nel sistema."
)
async def users_list(request: Request, user_service: UserServiceMeta = Depends(UserService)) -> BaseResponse[list[UserResponse]]:
    AuthChecker.assert_has_role(request, [Roles.ADMIN.value])
    return success_response(user_service.find_all())
