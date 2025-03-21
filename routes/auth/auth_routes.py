from fastapi import APIRouter, Depends, Response, Request

from controllers.auth_controller import AuthController
from models.request.auth.auth_request import LoginRequest, RefreshTokenRequest

router = APIRouter()

@router.post("/login")
async def login(login: LoginRequest, response: Response, request: Request, auth_controller: AuthController = Depends(AuthController)):
    # response.set_cookie(
    #     key="key",
    #     value="test",
    #     domain="0.0.0.0",
    #     max_age=3600
    # )
    response.set_cookie(key="test", value="test", domain="0.0.0.0")
    return auth_controller.login(login, response, request)

@router.post("/test")
async def test(response: Response):
    response.set_cookie(key="test", value="test", domain="0.0.0.0")
    return {"test": "test"}

@router.post("/refresh_token")
async def refresh_token(request: RefreshTokenRequest, auth_controller: AuthController = Depends(AuthController)):
    return await auth_controller.refresh_token(request)