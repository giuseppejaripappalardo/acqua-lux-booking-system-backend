from fastapi import APIRouter, Depends, Response, Request

from models.request.auth.auth_request import LoginRequest
from services.impl.auth_service import AuthService
from services.meta.auth_service_meta import AuthServiceMeta
from utils.format_response import success_response

router = APIRouter()

@router.post("/login")
async def login(credentials: LoginRequest, response: Response, request: Request, auth_service: AuthServiceMeta = Depends(AuthService)):
    print(credentials)
    return success_response(auth_service.login(credentials))