from fastapi import APIRouter, Depends, Request

from models.response.base_response import BaseResponse
from models.response.role.role_response import RoleResponse
from services.impl.role_service import RoleService
from services.meta.role_service_meta import RoleServiceMeta
from utils.auth_checker import AuthChecker
from utils.format_response import success_response
from utils.roles import Roles

router = APIRouter()

@router.get(
    "/list",
    response_model=BaseResponse[list[RoleResponse]],
    summary="Questo endpoint permette di creare un nuovo utente nel sistema.",
    description="Fornisce la possibilità di aggiungere un nuovo utente fornendo i dati necessari."
)
async def role_list(request: Request, role_service: RoleServiceMeta = Depends(RoleService)) -> BaseResponse[list[RoleResponse]]:
    AuthChecker.assert_has_role(request, [Roles.ADMIN.value])
    return success_response(role_service.find_all())