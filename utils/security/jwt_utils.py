import os

import jwt
from fastapi import Request

from exceptions.auth.auth_exception import AuthException
from models.object.token_payload import TokenPayload
from utils.enum.messages import Messages


class JwtUtils:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
    ALGORITHM = os.getenv("JWT_ALGORITHM", None)

    @classmethod
    def create_access_token(cls, data: TokenPayload) -> str:
        payload = data.model_dump()
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str) -> TokenPayload:
        decoded_dict: dict = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        return TokenPayload.model_validate(decoded_dict)

    @staticmethod
    def extract_token(request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthException(code=401, message=Messages.MISSING_AUTHENTICATION_HEADER.value)
        return auth_header.replace("Bearer ", "")