from exceptions.base_exception import AcquaLuxBaseException


class UserAlreadyExists(AcquaLuxBaseException):
    """
        Prevedo un messaggio generico come 'User already exists', in questo caso il
        messaggio verrà mostrato solo ad utenti con ruole amministratore e che comunque sono autenticati.
        Normalmente se avessi un servizio di registrazione, non metterei mai un messaggio cosi specifico
        sopratutto per ragioni di sicurezza.
    """
    def __init__(self, message: str = "User already exists", code: int = 400):
        super().__init__(message, code)
