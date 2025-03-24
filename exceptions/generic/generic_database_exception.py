from exceptions.base_exception import AcquaLuxBaseException


class GenericDatabaseException(AcquaLuxBaseException):
    def __init__(self, message: str = "Generic database error.", code: int = 500):
        super().__init__(message, code)
