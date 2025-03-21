from exceptions.base_exception import AcquaLuxBaseException


class IntegrityDatabaseException(AcquaLuxBaseException):
    """
        Eccezione sollevata quando si verifica una violazione dei vincoli di integrità nel database.

        Questa eccezione viene generalmente lanciata in caso di:
            Violazione di vincoli di unicità (chiave duplicata vedi ad esempio user con username unique)
            Violazione di vincoli di chiave esterna
            Altri vincoli di integrità definiti nello schema
    """

    def __init__(self,
                 message: str = "Violation of database integrity constraints",
                 code: int = 400,
                 constraint_name: str = None,
                 table_name: str = None):
        self.constraint_name = constraint_name
        self.table_name = table_name


        """
            Se siamo in grado di dare informazioni aggiuntive, mostriamo un messaggio
            più specifico che ci aiuti a debuggare il problema.
        """
        if constraint_name and table_name:
            message = f"Violation of constraint '{constraint_name}' on table '{table_name}'"
        elif constraint_name:
            message = f"Violation of constraint '{constraint_name}' in the database"
        elif table_name:
            message = f"Integrity constraint violation on table '{table_name}'"

        super().__init__(message, code)

    def get_details(self) -> dict:
        """
            Metodo di utilità per che restituisce i dettagli dell'errore in formato più strutturato
        """
        return {
            "message": self.message,
            "code": self.code,
            "constraint_name": self.constraint_name,
            "table_name": self.table_name,
            "error_type": "integrity_violation"
        }