from exceptions.base_exception import AcquaLuxBaseException


class AuthException(AcquaLuxBaseException):
    """
        Eccezione specifica per le operazioni di autenticazione.
        Verrà utilizzata nel caso di credenziali errate o utente non autorizzato.
    """
    def __init__(self, message, code=401):
        super().__init__(message, code)