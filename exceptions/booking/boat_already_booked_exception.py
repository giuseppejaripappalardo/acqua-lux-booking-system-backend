from exceptions.base_exception import AcquaLuxBaseException


class BoatAlreadyBookedException(AcquaLuxBaseException):
    """
        Eccezione specifica per tentativi di prenotazione su imbarcazioni non disponibili.
    """
    def __init__(self, message, code=400):
        super().__init__(message, code)