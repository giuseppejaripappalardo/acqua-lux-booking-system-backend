from fastapi import Depends, Response, Request

from controllers.base_controller import BaseController
from decorators.handle_exceptions import handle_exceptions
from services.impl.auth_service import AuthService
from logger_service import LoggerService
from services.meta.auth_service_meta import AuthServiceMeta
from models.request.auth.auth_request import LoginRequest, RefreshTokenRequest


class AuthController(BaseController):
    _auth_service: AuthServiceMeta = None
    _logger_service: LoggerService.logger = None

    def __init__(self, auth_service: AuthServiceMeta = Depends(AuthService),
                 logger_service: LoggerService = Depends(LoggerService)):
        self._auth_service = auth_service
        self._logger_service = logger_service

    @handle_exceptions
    def login(self, req: LoginRequest, response: Response, request: Request):

        result = self._auth_service.login(req.username, req.password)
        token_data = result["token_data"]
        cookie_info = result["cookie_info"]

        return token_data

    @handle_exceptions
    async def refresh_token(self, request: RefreshTokenRequest):
        return self._auth_service.refresh_token(request.refresh_token)
