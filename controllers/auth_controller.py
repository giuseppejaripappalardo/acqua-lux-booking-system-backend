from fastapi import APIRouter, Depends, Response, Request

from models.request.auth.auth_request import LoginRequest
from models.response.auth.auth_response import TokenResponse
from models.response.base_response import BaseResponse
from services.impl.auth_service import AuthService
from services.meta.auth_service_meta import AuthServiceMeta
from utils.format_response import success_response

router = APIRouter()

@router.post(
    "/login",
    response_model=BaseResponse[TokenResponse],
    summary="Questo endpoint permette di creare un nuovo utente nel sistema.",
    description="Fornisce la possibilità di aggiungere un nuovo utente fornendo i dati necessari.")
async def login(credentials: LoginRequest, response: Response, request: Request, auth_service: AuthServiceMeta = Depends(AuthService)):
    return success_response(auth_service.login(credentials))