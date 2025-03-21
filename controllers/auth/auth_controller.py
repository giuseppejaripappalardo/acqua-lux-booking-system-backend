from fastapi import APIRouter, Depends, Response, Request

from models.request.auth.auth_request import LoginRequest, RefreshTokenRequest
from services.impl.auth_service import AuthService
from services.meta.auth_service_meta import AuthServiceMeta
from utils.format_response import success_response

router = APIRouter()

@router.post("/login")
async def login(login: LoginRequest, response: Response, request: Request, auth_service: AuthServiceMeta = Depends(AuthService)):
    return success_response(auth_service.login(login))

@router.post("/refresh_token")
async def refresh_token(request: RefreshTokenRequest, auth_service: AuthServiceMeta = Depends(AuthService)):
    return await success_response(auth_service.refresh_token(request.refresh_token))
