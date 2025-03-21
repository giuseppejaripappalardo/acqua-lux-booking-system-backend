from pydantic import BaseModel


class TokenResponse(BaseModel):
    jwt_token: str