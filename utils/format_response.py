from models.response.base_response import BaseResponse


def success_response(data=None, message="Request completed successfully") -> BaseResponse:
    """
        Restituisce una risposta http di success standard.
    """
    return BaseResponse(
        success=True,
        message=message,
        data=data if data is not None else None
    )


def error_response(message="An error occurred") -> BaseResponse:
    """
        Formatta il contenuto di una risposta di errore standard.
    """
    return BaseResponse(
        success=False,
        message=message,
        data=None
    )
