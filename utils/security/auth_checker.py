from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer

from models.object.token_payload import TokenPayload
from utils.security.jwt_utils import JwtUtils
from exceptions.auth.auth_exception import AuthException
from exceptions.auth.role_exception import RoleException
from utils.enum.messages import Messages

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthChecker:
    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
        try:
            user: TokenPayload = JwtUtils.decode_token(token)
        except Exception:
            raise AuthException(code=401, message=Messages.INVALID_AUTH_TOKEN.value)
        return user

    @staticmethod
    def assert_user_is_authenticated(request: Request) -> TokenPayload:
        token: str = JwtUtils.extract_token(request)
        try:
            user: TokenPayload = JwtUtils.decode_token(token)
            request.state.user = user
        except Exception:
            raise AuthException(code=401, message=Messages.INVALID_AUTH_TOKEN.value)

        return user

    @staticmethod
    def get_logged_in_user(request: Request) -> TokenPayload:
        return AuthChecker.assert_user_is_authenticated(request)

    @staticmethod
    def assert_has_role(request: Request, allowed_roles: list[str]) -> None:
        token = JwtUtils.extract_token(request)
        try:
            user: TokenPayload = JwtUtils.decode_token(token)
            request.state.user = user
        except Exception:
            raise AuthException(code=401, message=Messages.INVALID_AUTH_TOKEN.value)

        user_role = user.role
        if user_role not in allowed_roles:
            raise RoleException(code=403, message=Messages.INSUFFICIENT_ROLE_PERMISSIONS.value)
