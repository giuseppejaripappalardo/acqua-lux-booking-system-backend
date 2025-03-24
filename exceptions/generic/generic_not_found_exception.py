from exceptions.base_exception import AcquaLuxBaseException
from utils.enum.messages import Messages


class GenericNotFoundException(AcquaLuxBaseException):
    def __init__(self, message: str = Messages.NOT_FOUND.value, code: int = 404):
        super().__init__(message, code)
