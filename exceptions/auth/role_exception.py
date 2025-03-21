from exceptions.base_exception import AcquaLuxBaseException


class RoleException(AcquaLuxBaseException):
    """
        Questa eccezione viene lanciata se il ruolo dell'utente
        Non è sufficiente per accedere ad una specifica risorsa.
    """
    def __init__(self, message, code=401):
        super().__init__(message, code)
