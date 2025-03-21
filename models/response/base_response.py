from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel,Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None