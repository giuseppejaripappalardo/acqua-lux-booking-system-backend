import jwt
from datetime import datetime, timedelta
from typing import Tuple
import os
import pytz


class JwtUtils:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
    ALGORITHM = os.getenv("JWT_ALGORITHM", None)
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", None)
    REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", None)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(pytz.utc) + timedelta(minutes=int(self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)


    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(pytz.utc) + timedelta(days=int(self.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])