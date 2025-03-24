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
async def login(response: Response, credentials: LoginRequest, auth_service: AuthServiceMeta = Depends(AuthService)):
    return success_response(auth_service.login(response, credentials))

@router.post(
    "/refresh_token",
    response_model=BaseResponse[TokenResponse],
    summary="Simula un meccanismo di refresh token per l'autenticazione.",
    description="Legge il token JWT esistente dal cookie sicuro. Questa soluzione semplificata è utilizzata perché l'autenticazione è fuori dagli obiettivi del project work, evitando l'uso di localStorage (vulnerabile a XSS) ma senza implementare un vero sistema di refresh token.")
async def refresh_token(request: Request, auth_service: AuthServiceMeta = Depends(AuthService)):
    return success_response(auth_service.refresh(request))
