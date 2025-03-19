from exceptions.base_exception import AcquaLuxBaseException


class UserAlreadyExists(AcquaLuxBaseException):
    def __init__(self, message: str = "Utente già esistente", code: int = 400):
        super().__init__(message, code)
