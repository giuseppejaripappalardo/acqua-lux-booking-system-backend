from fastapi.responses import JSONResponse


class BaseController:
    """
    Controller base che fornisce metodi di interfaccia standard per le risposte.
    Questo sarà esteso da altri controller ed utilizzato nelle route.
    """

    @staticmethod
    def send_success(data=None, message="Richiesta completata con successo", status_code=200):
        """
        Restituisce una risposta di successo standard.

        :param data: Dati da includere nella risposta
        :param message: Messaggio di successo
        :param status_code: Codice di stato HTTP (default: 200)
        :return: JSONResponse
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data,
            },
        )

    @staticmethod
    def send_error(message="Si è verificato un errore", status_code=400, errors=None):
        """
        Restituisce una risposta di errore standard.

        :param message: Messaggio di errore
        :param status_code: Codice di stato HTTP (default: 400)
        :param errors: Dettagli aggiuntivi sull'errore
        :return: JSONResponse
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "errors": errors,
            },
        )
