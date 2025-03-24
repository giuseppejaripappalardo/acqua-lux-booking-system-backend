from typing import Optional

from pydantic import BaseModel

from models.response.user.user_response import UserResponse


class TokenResponse(BaseModel):
    jwt_token: str
    user: Optional[UserResponse] = None