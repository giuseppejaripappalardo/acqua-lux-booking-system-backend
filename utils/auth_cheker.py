from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_utils import JwtUtils
from exceptions.auth.auth_exception import AuthException
from exceptions.auth.role_exception import RoleException
from utils.messages import Messages

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class AuthChecker:
    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
        try:
            user = JwtUtils.decode_token(token)
        except Exception:
            raise AuthException(code=401, message=Messages.INVALID_AUTH_TOKEN.value)
        return user

    @staticmethod
    def assert_has_role(request: Request, allowed_roles: list[str]) -> dict:
        user = getattr(request.state, "user", None)
        if not user:
            token = JwtUtils.extract_token(request)
            try:
                user = JwtUtils.decode_token(token)
                request.state.user = user
            except Exception:
                raise AuthException(code=401, message=Messages.INVALID_AUTH_TOKEN.value)

        user_role = user.get("role")
        if user_role not in allowed_roles:
            raise RoleException(code=403, message=Messages.INSUFFICIENT_ROLE_PERMISSIONS.value)
        return user
