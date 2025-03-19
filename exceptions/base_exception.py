
class AcquaLuxBaseException(Exception):
    """
        Classe base per definire eccezioni personalizzate nel progetto.

        Questa classe viene ereditata per creare eccezioni specifiche
        per diversi moduli e contesti dell'applicazione. È il punto di partenza
        per implementare logiche di gestione degli errori.
    """
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code