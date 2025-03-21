from fastapi import Depends

from controllers.base_controller import BaseController
from decorators.handle_exceptions import handle_exceptions
from impl.user_service import UserService
from logger_service import LoggerService
from meta.user_service_meta import UserServiceMeta
from request.user.user_request import UserRequest


class UserController(BaseController):
    _user_service: UserServiceMeta = None
    _logger_service: LoggerService.logger = None

    def __init__(self, user_service: UserServiceMeta = Depends(UserService),
                 logger_service: LoggerService = Depends(LoggerService)):
        self._user_service = user_service
        self._logger_service = logger_service

    @handle_exceptions
    async def create_user(self, user: UserRequest):
        return self._user_service.create_user(user)

    @handle_exceptions
    async def find_all(self):
        return self._user_service.find_all()
