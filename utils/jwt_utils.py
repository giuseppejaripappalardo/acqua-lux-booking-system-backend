import os
from datetime import datetime, timedelta

import jwt
import pytz
from fastapi import Request

from exceptions.auth.auth_exception import AuthException
from utils.messages import Messages


class JwtUtils:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
    ALGORITHM = os.getenv("JWT_ALGORITHM", None)
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", None)

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(pytz.utc) + timedelta(minutes=int(cls.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])

    @staticmethod
    def extract_token(request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthException(code=401, message=Messages.MISSING_AUTHENTICATION_HEADER.value)
        return auth_header.replace("Bearer ", "")