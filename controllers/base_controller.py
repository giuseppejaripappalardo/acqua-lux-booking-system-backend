from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class BaseController:
    """
    Controller base che fornisce metodi di interfaccia standard per le risposte.
    """

    def send_success(self, data=None, message="Request completed successfully", status_code=200):
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
                "data": jsonable_encoder(data),
            },
        )

    def send_error(self, message="An error has occurred", status_code=400, errors=None):
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
