from fastapi import APIRouter, Depends, Request

from models.response.base_response import BaseResponse
from models.response.role.role_response import RoleResponse
from services.impl.role_service import RoleService
from services.meta.role_service_meta import RoleServiceMeta
from utils.security.auth_checker import AuthChecker
from utils.format_response import success_response
from utils.enum.roles import Roles

router = APIRouter()

@router.get(
    "/list",
    response_model=BaseResponse[list[RoleResponse]],
    summary="Questo endpoint permette di ottenere la lista dei ruoli disponibili nel sistema.",
    description="Recupera e restituisce un elenco di tutti i ruoli registrati nel sistema.",
    responses={
        401: {
            "description": "Errore di autenticazione - Utente non autenticato",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Invalid authentication token"}
                }
            }
        },
        403: {
            "description": "Errore di autorizzazione - Utente non autorizzato (richiesto ruolo ADMIN)",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "User does not have the required role"}
                }
            }
        },
        500: {
            "description": "Errore interno del server",
            "content": {
                "application/json": {
                    "example": {"success": False, "message": "Internal server error"}
                }
            }
        }
    }
)
async def role_list(request: Request, role_service: RoleServiceMeta = Depends(RoleService)) -> BaseResponse[list[RoleResponse]]:
    AuthChecker.assert_has_role(request, [Roles.ADMIN.value])
    return success_response(role_service.find_all())
