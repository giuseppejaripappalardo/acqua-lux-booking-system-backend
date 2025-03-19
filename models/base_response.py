from pydantic import BaseModel
from typing import Optional, Any, Union


class BaseResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None


class BaseError(BaseModel):
    error_code: Optional[int] = None


class SuccessResponse(BaseResponse):
    status: str = "success"
    message: str = "Request successful"
    data: Any


class ErrorResponse(BaseResponse, BaseError):
    status: str = "error"
    message: Optional[str] = None
    data: Optional[Union[dict, list]] = None
