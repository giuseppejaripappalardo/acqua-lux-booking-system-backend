from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TokenPayload(BaseModel):

    sub: str
    role: str
    exp: datetime

    model_config = ConfigDict(
        from_attributes=True
    )