from exceptions.base_exception import AcquaLuxBaseException


class GenericDatabaseException(AcquaLuxBaseException):
    def __init__(self, message: str = "Errore generico nel database", code: int = 500):
        super().__init__(message, code)
