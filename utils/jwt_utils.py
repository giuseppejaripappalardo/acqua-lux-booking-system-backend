import os
from datetime import datetime, timedelta
from http.client import HTTPException

import jwt
import pytz
from fastapi import Request, HTTPException

from exceptions.auth.auth_exception import AuthException
from exceptions.auth.role_exception import RoleException
from utils.messages import Messages


class JwtUtils:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
    ALGORITHM = os.getenv("JWT_ALGORITHM", None)
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", None)
    REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", None)

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(pytz.utc) + timedelta(minutes=int(cls.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(pytz.utc) + timedelta(days=int(cls.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])

    @staticmethod
    def extract_token(request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail=Messages.MISSING_AUTHENTICATION_HEADER.value)
        return auth_header.replace("Bearer ", "")