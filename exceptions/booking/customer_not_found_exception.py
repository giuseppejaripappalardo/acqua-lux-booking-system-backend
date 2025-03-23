from exceptions.base_exception import AcquaLuxBaseException


class CustomerNotFoundException(AcquaLuxBaseException):
    """
        Eccezione specifica quando il customer selezionato per la prenotazione non esiste.
    """

    def __init__(self, message="Customer not found", code=404):
        super().__init__(message, code)