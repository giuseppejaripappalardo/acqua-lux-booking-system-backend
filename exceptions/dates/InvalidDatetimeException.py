from exceptions.base_exception import AcquaLuxBaseException


class InvalidDatetimeException(AcquaLuxBaseException):
    def __init__(self, message, code=422):
        super().__init__(message, code)